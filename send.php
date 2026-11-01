<?php
/**
 * Mobiele Badkamer — rental request mailer.
 *
 * Upload this file to the web root (next to index.html) on a host that runs PHP
 * (any normal shared host, including the one WordPress runs on now).
 * The contact form uses it automatically there; on GitHub Pages, which can't run PHP,
 * the form uses FormSubmit instead (see assets/js/site.js).
 *
 * Only the CONFIG block below normally needs changing.
 */

declare(strict_types=1);

/* ---------------- CONFIG ---------------- */
const MAIL_TO   = 'info@mobielebadkamer.info';           // where requests go
const MAIL_FROM = 'website@mobielebadkamer.info';        // must be an address on YOUR domain (SPF/DKIM)
const ALLOWED_HOSTS = ['mobielebadkamer.info', 'www.mobielebadkamer.info']; // sites allowed to post here
const RATE_LIMIT_MAX    = 5;     // max requests ...
const RATE_LIMIT_WINDOW = 3600;  // ... per IP address per this many seconds
/* ---------------------------------------- */

ini_set('display_errors', '0');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');
header('Referrer-Policy: strict-origin-when-cross-origin');

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond(int $status, array $payload, bool $json): void
{
    http_response_code($status);
    if ($json) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($payload, JSON_UNESCAPED_UNICODE);
    } else {
        // Plain fallback page for browsers without JavaScript.
        header('Content-Type: text/html; charset=utf-8');
        $ok  = !empty($payload['ok']);
        $msg = htmlspecialchars($payload['message'] ?? '', ENT_QUOTES, 'UTF-8');
        $title = $ok ? 'Bedankt, je aanvraag is verstuurd' : 'Versturen lukte niet';
        echo "<!doctype html><html lang=\"nl\"><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
           . "<title>{$title}</title><body style=\"font:18px/1.6 system-ui,sans-serif;max-width:36rem;margin:4rem auto;padding:0 1rem\">"
           . "<h1>{$title}</h1><p>{$msg}</p><p><a href=\"contact/index.html\">Terug naar het formulier</a> · Bel <a href=\"tel:+31654254740\">06 54 25 47 40</a></p></body></html>";
    }
    exit;
}

/* ---- 1. Only POST, small bodies, from our own site ---- */
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(405, ['ok' => false, 'message' => 'Alleen POST is toegestaan.'], true);
}
if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 20000) {
    respond(413, ['ok' => false, 'message' => 'Aanvraag is te groot.'], $wantsJson);
}

$origin = $_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '';
if ($origin !== '') {
    $originHost = strtolower((string)parse_url($origin, PHP_URL_HOST));
    $ownHost    = strtolower(explode(':', $_SERVER['HTTP_HOST'] ?? '')[0]);
    if ($originHost !== $ownHost && !in_array($originHost, ALLOWED_HOSTS, true)) {
        respond(403, ['ok' => false, 'message' => 'Aanvraag van een onbekende website.'], $wantsJson);
    }
}

/* ---- 2. Honeypot: bots fill the hidden field. Pretend success, send nothing. ---- */
if (trim((string)($_POST['_honey'] ?? '')) !== '') {
    respond(200, ['ok' => true, 'message' => 'Bedankt.'], $wantsJson);
}

/* ---- 3. Rate limit per IP (only a hash of the IP is stored, for at most one hour) ---- */
$ipHash = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . __FILE__);
$rlFile = sys_get_temp_dir() . '/mb-rl-' . substr($ipHash, 0, 32) . '.json';
$now    = time();
$hits   = [];
if (is_file($rlFile)) {
    $hits = json_decode((string)@file_get_contents($rlFile), true) ?: [];
}
$hits = array_values(array_filter($hits, static fn($t) => is_int($t) && $t > $now - RATE_LIMIT_WINDOW));
if (count($hits) >= RATE_LIMIT_MAX) {
    respond(429, ['ok' => false, 'message' => 'Je hebt al een paar aanvragen verstuurd. Bel ons gerust op 06 54 25 47 40.'], $wantsJson);
}

/* ---- 4. Validate every field (allowlists and limits) ---- */
function field(string $name, int $max): string
{
    $v = $_POST[$name] ?? '';
    if (!is_string($v)) return '';
    $v = trim(str_replace("\0", '', $v));
    return mb_substr($v, 0, $max, 'UTF-8');
}
function oneLine(string $v): string
{
    return trim(preg_replace('/[\r\n\t]+/', ' ', $v) ?? '');
}

$errors = [];
$products = [
    'badkamer'     => ['label' => 'Mobiele badkamer',     'minDays' => 14, 'vat' => 'excl. btw'],
    'douchecabine' => ['label' => 'Mobiele douchecabine', 'minDays' => 7,  'vat' => 'incl. btw'],
];

$productKey = field('product', 20);
if (!isset($products[$productKey])) {
    $errors['product'] = 'Kies wat je wilt huren.';
    $productKey = 'badkamer';
}
$product = $products[$productKey];

$tz    = new DateTimeZone('Europe/Amsterdam');
$today = new DateTimeImmutable('today', $tz);
$parseDate = static function (string $v) use ($tz): ?DateTimeImmutable {
    $d = DateTimeImmutable::createFromFormat('!Y-m-d', $v, $tz);
    return ($d && $d->format('Y-m-d') === $v) ? $d : null;
};

$from = $parseDate(field('vanaf', 10));
$to   = $parseDate(field('tot', 10));
$days = 0;
if (!$from) {
    $errors['vanaf'] = 'Kies de eerste dag dat je de badkamer nodig hebt.';
} elseif ($from < $today) {
    $errors['vanaf'] = 'Deze datum ligt in het verleden.';
} elseif ($from > $today->modify('+2 years')) {
    $errors['vanaf'] = 'Kies een datum binnen twee jaar.';
}
if (!$to) {
    $errors['tot'] = 'Kies tot wanneer je hem ongeveer nodig hebt.';
} elseif ($from) {
    $days = (int)$from->diff($to)->format('%r%a') + 1;
    if ($days < $product['minDays']) {
        $errors['tot'] = sprintf('Kies minimaal %d dagen (nu %d).', $product['minDays'], max($days, 0));
    } elseif ($days > 730) {
        $errors['tot'] = 'Neem voor een huurperiode van meer dan twee jaar even contact op.';
    }
}

$first = oneLine(field('voornaam', 80));
$last  = oneLine(field('achternaam', 80));
if ($first === '') $errors['voornaam'] = 'Vul je voornaam in.';
if ($last === '')  $errors['achternaam'] = 'Vul je achternaam in.';

$email = oneLine(field('email', 254));
if ($email === '') {
    $errors['email'] = 'Vul je e-mailadres in.';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL) || !preg_match('/\.[a-z]{2,}$/i', $email)) {
    $errors['email'] = 'Dit lijkt geen geldig e-mailadres. Controleer de @ en de punt.';
}

$phone = oneLine(field('telefoon', 30));
if ($phone === '') {
    $errors['telefoon'] = 'Vul je telefoonnummer in.';
} elseif (!preg_match('/^[0-9\s+\-()]{8,30}$/', $phone) || strlen(preg_replace('/\D/', '', $phone)) < 8) {
    $errors['telefoon'] = 'Gebruik alleen cijfers, spaties of een +, bijvoorbeeld 06 12345678.';
}

$place    = oneLine(field('plaats', 80));
$delivery = field('levering', 20) === 'zelf' ? 'Haalt zelf op (trekhaak / auto)' : 'Graag bezorgen en aansluiten';
$notes    = field('opmerkingen', 2000);

if ($errors) {
    respond(422, ['ok' => false, 'message' => 'Controleer de gemarkeerde velden.', 'errors' => $errors], $wantsJson);
}

/* ---- 5. Compose the email (server-side price, never trust the browser's) ---- */
function nlDate(DateTimeImmutable $d): string
{
    $days   = ['zondag', 'maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag'];
    $months = ['januari', 'februari', 'maart', 'april', 'mei', 'juni', 'juli', 'augustus', 'september', 'oktober', 'november', 'december'];
    return $days[(int)$d->format('w')] . ' ' . $d->format('j') . ' ' . $months[(int)$d->format('n') - 1] . ' ' . $d->format('Y');
}
$weeks = max((int)ceil($days / 7), intdiv($product['minDays'], 7));
$price = $productKey === 'badkamer' ? $weeks * 137.50 : 129 + ($weeks - 1) * 99;
$priceText = '€' . number_format($price, 2, ',', '.') . ' ' . $product['vat'] . " ({$weeks} " . ($weeks === 1 ? 'week' : 'weken') . ')';

$subject = sprintf('Huuraanvraag %s: %s t/m %s', $product['label'], nlDate($from), nlDate($to));
$rows = [
    'Product'            => $product['label'],
    'Vanaf'              => nlDate($from),
    'Tot en met'         => nlDate($to),
    'Aantal dagen'       => (string)$days,
    'Indicatie huurprijs'=> $priceText,
    'Naam'               => "$first $last",
    'E-mail'             => $email,
    'Telefoon'           => $phone,
    'Plaats / postcode'  => $place !== '' ? $place : '-',
    'Bezorging'          => $delivery,
];
$body = "Nieuwe huuraanvraag via mobielebadkamer.info\n\n";
foreach ($rows as $k => $v) {
    $body .= str_pad($k . ':', 22) . $v . "\n";
}
$body .= "\nOpmerkingen:\n" . ($notes !== '' ? $notes : '-') . "\n\n"
       . "Beantwoorden gaat direct naar de klant.\n"
       . 'Verstuurd op ' . (new DateTimeImmutable('now', $tz))->format('d-m-Y H:i') . "\n";

$fromName = '=?UTF-8?B?' . base64_encode('Website Mobiele Badkamer') . '?=';
$headers = [
    'From: ' . $fromName . ' <' . MAIL_FROM . '>',
    'Reply-To: ' . $email,             // validated above; contains no line breaks
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: mobielebadkamer-send',
];
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';

$sent = @mail(MAIL_TO, $encodedSubject, $body, implode("\r\n", $headers), '-f' . MAIL_FROM);
if (!$sent) {
    // Some hosts refuse the -f parameter; retry without it.
    $sent = @mail(MAIL_TO, $encodedSubject, $body, implode("\r\n", $headers));
}
if (!$sent) {
    error_log('send.php: mail() failed');
    respond(500, ['ok' => false, 'message' => 'Versturen lukte niet. Bel ons op 06 54 25 47 40 of mail naar ' . MAIL_TO . '.'], $wantsJson);
}

$hits[] = $now;
@file_put_contents($rlFile, json_encode($hits), LOCK_EX);

respond(200, ['ok' => true, 'message' => 'We nemen zo snel mogelijk contact met je op over de beschikbaarheid.'], $wantsJson);
