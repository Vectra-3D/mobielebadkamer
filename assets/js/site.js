/* Mobiele Badkamer — progressive enhancement only. Every page reads fine without this file. */
(() => {
  "use strict";

  /* ---------- config ----------
     How the request form sends, in order:
     1. On your own web host: send.php (in the site root) mails the request. No third party.
     2. If send.php isn't there or PHP doesn't run (e.g. GitHub Pages): FormSubmit (formsubmit.co).
        The very first FormSubmit request triggers a one-time activation email to MAIL_TO;
        click the link in it and every request after that arrives directly. FormSubmit then
        also mails a random alias: put it in place of MAIL_TO in FORMSUBMIT_ENDPOINT.
     3. If both fail, the visitor gets a ready-made email link and the phone number.
     Set FORMSUBMIT_ENDPOINT to "" to never use FormSubmit. */
  const MAIL_TO = "info@mobielebadkamer.info";
  const FORMSUBMIT_ENDPOINT = `https://formsubmit.co/ajax/${MAIL_TO}`;

  const PRICES = {
    badkamer: { label: "Mobiele badkamer", minDays: 14, vat: "excl. btw", week: (n) => n * 137.5, detail: (n) => `${n} ${n === 1 ? "week" : "weken"} × €137,50` },
    douchecabine: { label: "Mobiele douchecabine", minDays: 7, vat: "incl. btw", week: (n) => (n <= 0 ? 0 : 129 + (n - 1) * 99), detail: (n) => (n <= 1 ? "1 week × €129,00" : `€129,00 eerste week + ${n - 1} × €99,00`) },
  };
  const euro = (v) => new Intl.NumberFormat("nl-NL", { style: "currency", currency: "EUR" }).format(v).replace(/\s/g, "");
  const iso = (d) => new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const dayDiff = (a, b) => Math.round((new Date(b) - new Date(a)) / 86400000) + 1; // inclusive
  const nlDate = (v) => (v ? new Date(`${v}T12:00:00`).toLocaleDateString("nl-NL", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) : "-");

  /* ---------- mobile menu ---------- */
  const menu = document.getElementById("menu");
  document.querySelectorAll("[data-menu-open]").forEach((b) => b.addEventListener("click", () => { menu?.showModal(); b.setAttribute("aria-expanded", "true"); }));
  document.querySelectorAll("[data-menu-close]").forEach((b) => b.addEventListener("click", () => menu?.close()));
  menu?.addEventListener("close", () => document.querySelectorAll("[data-menu-open]").forEach((b) => b.setAttribute("aria-expanded", "false")));
  menu?.addEventListener("click", (e) => { if (e.target === menu) menu.close(); });

  /* ---------- video facade (loads Vimeo only on click) ---------- */
  document.querySelectorAll("[data-vimeo]").forEach((wrap) => {
    const btn = wrap.querySelector("button");
    btn?.addEventListener("click", () => {
      const id = wrap.dataset.vimeo;
      const iframe = document.createElement("iframe");
      iframe.src = `https://player.vimeo.com/video/${id}?dnt=1&autoplay=1&title=0&byline=0&portrait=0`;
      iframe.allow = "autoplay; fullscreen; picture-in-picture";
      iframe.title = wrap.dataset.title || "Video";
      wrap.replaceChildren(iframe);
    }, { once: true });
  });

  /* ---------- gallery lightbox ---------- */
  const lb = document.getElementById("lightbox");
  if (lb) {
    const items = [...document.querySelectorAll("[data-lightbox]")];
    const img = lb.querySelector("img");
    const cap = lb.querySelector("figcaption");
    let i = 0;
    const show = (n) => {
      i = (n + items.length) % items.length;
      const it = items[i];
      img.src = it.dataset.lightbox;
      img.alt = it.querySelector("img")?.alt || "";
      cap.textContent = `${it.querySelector("img")?.alt || ""} (${i + 1}/${items.length})`;
    };
    items.forEach((it, n) => it.addEventListener("click", () => { show(n); lb.showModal(); }));
    lb.querySelector("[data-prev]")?.addEventListener("click", () => show(i - 1));
    lb.querySelector("[data-next]")?.addEventListener("click", () => show(i + 1));
    lb.querySelector("[data-close]")?.addEventListener("click", () => lb.close());
    lb.addEventListener("click", (e) => { if (e.target === lb) lb.close(); });
    lb.addEventListener("keydown", (e) => { if (e.key === "ArrowLeft") show(i - 1); if (e.key === "ArrowRight") show(i + 1); });
  }

  /* ---------- quick availability form (home + band) ---------- */
  document.querySelectorAll("form[data-quick]").forEach((f) => {
    const from = f.querySelector('[name="vanaf"]');
    const to = f.querySelector('[name="tot"]');
    const today = iso(new Date());
    if (from) from.min = today;
    from?.addEventListener("change", () => {
      if (!to) return;
      const min = iso(addDays(new Date(from.value), 13));
      to.min = min;
      if (!to.value || to.value < min) to.value = min;
    });
  });

  /* ---------- rental request form ---------- */
  const form = document.getElementById("aanvraag");
  if (!form) return;

  const q = new URLSearchParams(location.search);
  const $ = (s) => form.querySelector(s);
  const from = $('[name="vanaf"]');
  const to = $('[name="tot"]');
  const est = document.getElementById("estimate");
  const product = () => form.querySelector('[name="product"]:checked')?.value || "badkamer";

  // prefill from quick form / product links
  if (q.get("product") && PRICES[q.get("product")]) {
    const r = form.querySelector(`[name="product"][value="${q.get("product")}"]`);
    if (r) r.checked = true;
  }
  if (q.get("vanaf")) from.value = q.get("vanaf");
  if (q.get("tot")) to.value = q.get("tot");
  from.min = iso(new Date());

  const setError = (input, msg) => {
    const field = input.closest(".field");
    const box = field?.querySelector(".error span");
    if (msg) { field?.classList.add("has-error"); input.setAttribute("aria-invalid", "true"); if (box) box.textContent = msg; }
    else { field?.classList.remove("has-error"); input.removeAttribute("aria-invalid"); }
  };

  const update = () => {
    const p = PRICES[product()];
    if (from.value) to.min = iso(addDays(new Date(from.value), p.minDays - 1));
    document.querySelectorAll("[data-min-note]").forEach((n) => (n.textContent = p.minDays === 14 ? "Minimale huurperiode is 14 dagen." : "Huur per week; langer huren is voordeliger."));
    if (!est) return;
    const amount = est.querySelector(".estimate__amount");
    const detail = est.querySelector(".estimate__detail");
    if (from.value && to.value && to.value >= from.value) {
      const days = dayDiff(from.value, to.value);
      const weeks = Math.max(Math.ceil(days / 7), p.minDays / 7);
      amount.textContent = euro(p.week(weeks));
      detail.textContent = `${days} dagen · ${p.detail(weeks)} · ${p.vat}. Indicatie op basis van hele weken; je ontvangt een definitieve prijs van ons.`;
      if (days < p.minDays) setError(to, `Kies minimaal ${p.minDays} dagen (nu ${days}).`); else setError(to, "");
    } else {
      amount.textContent = "—";
      detail.textContent = `Kies je periode, dan rekenen we het voor je uit. ${p.label}: ${p.vat}.`;
    }
  };
  form.addEventListener("change", update);
  form.addEventListener("input", (e) => { if (e.target.closest(".has-error")) validateField(e.target); });
  update();

  const validateField = (el) => {
    if (!el.name || el.type === "radio" || el.type === "hidden" || el.name.startsWith("_")) return true;
    let msg = "";
    if (el.validity.valueMissing) msg = el.dataset.required || "Dit veld is nodig om je aanvraag te behandelen.";
    else if (el.type === "email" && (el.validity.typeMismatch || !/@[^@\s]+\.[a-z]{2,}$/i.test(el.value.trim()))) msg = "Dit lijkt geen geldig e-mailadres. Controleer de @ en de punt.";
    else if (el.validity.patternMismatch) msg = el.dataset.pattern || "Controleer dit veld.";
    else if (el.validity.rangeUnderflow) msg = el === from ? "Deze datum ligt in het verleden." : `Kies minimaal ${PRICES[product()].minDays} dagen.`;
    setError(el, msg);
    return !msg;
  };

  form.setAttribute("novalidate", "");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (form.querySelector('[name="_honey"]')?.value) return; // honeypot
    const fields = [...form.querySelectorAll("input, select, textarea")];
    const ok = fields.map(validateField).every(Boolean);
    update();
    const firstBad = form.querySelector('[aria-invalid="true"]');
    if (!ok || firstBad) { firstBad?.focus(); return; }

    const data = new FormData(form);
    const p = PRICES[product()];
    const days = dayDiff(data.get("vanaf"), data.get("tot"));
    const estimate = document.querySelector("#estimate .estimate__amount")?.textContent || "-";
    const delivery = data.get("levering") === "zelf" ? "Haalt zelf op" : "Graag bezorgen en aansluiten";
    const subject = `Huuraanvraag ${p.label}: ${nlDate(data.get("vanaf"))} t/m ${nlDate(data.get("tot"))}`;
    // readable labels become the rows of the email table
    const mail = new FormData();
    mail.append("Product", p.label);
    mail.append("Vanaf", nlDate(data.get("vanaf")));
    mail.append("Tot en met", nlDate(data.get("tot")));
    mail.append("Aantal dagen", String(days));
    mail.append("Indicatie huurprijs", `${estimate} ${p.vat}`);
    mail.append("Naam", `${data.get("voornaam")} ${data.get("achternaam")}`.trim());
    mail.append("email", data.get("email"));
    mail.append("Telefoon", data.get("telefoon"));
    mail.append("Plaats / postcode", data.get("plaats") || "-");
    mail.append("Bezorging", delivery);
    mail.append("Opmerkingen", data.get("opmerkingen") || "-");
    mail.append("_subject", subject);
    mail.append("_template", "table");
    mail.append("_replyto", data.get("email"));
    mail.append("_captcha", "false");
    mail.append("_honey", "");

    const body = [
      `Product: ${p.label}`,
      `Periode: ${nlDate(data.get("vanaf"))} t/m ${nlDate(data.get("tot"))}`,
      `Naam: ${data.get("voornaam")} ${data.get("achternaam")}`,
      `E-mail: ${data.get("email")}`,
      `Telefoon: ${data.get("telefoon")}`,
      `Plaats / postcode: ${data.get("plaats") || "-"}`,
      `Bezorging: ${delivery}`,
      "",
      `${data.get("opmerkingen") || ""}`,
    ].join("\n");

    const btn = form.querySelector('[type="submit"]');
    const done = document.getElementById("form-done");
    const err = document.getElementById("form-error");
    const mailto = `mailto:${MAIL_TO}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

    // 1. send.php on our own host (skipped on GitHub Pages and when opened from disk)
    const sendPhp = async () => {
      const res = await fetch(form.dataset.php, { method: "POST", body: data, headers: { Accept: "application/json" } });
      const json = await res.json().catch(() => null);
      if (!json) return "unavailable"; // no PHP: 404/405 page, or the raw .php file
      if (res.ok && json.ok) return "sent";
      if (res.status === 422 && json.errors) {
        Object.entries(json.errors).forEach(([name, msg]) => { const el = form.querySelector(`[name="${name}"]`); if (el && el.type !== "radio") setError(el, msg); });
        return "invalid";
      }
      const e2 = new Error(json.message || `HTTP ${res.status}`); e2.status = res.status; throw e2;
    };
    // 2. FormSubmit (no server needed)
    const sendFormSubmit = async () => {
      const res = await fetch(FORMSUBMIT_ENDPOINT, { method: "POST", body: mail, headers: { Accept: "application/json" } });
      const json = await res.json().catch(() => ({}));
      if (!res.ok || String(json.success) !== "true") throw new Error(json.message || `HTTP ${res.status}`);
      return "sent";
    };
    const canUsePhp = form.dataset.php && /^https?:$/.test(location.protocol) && !/\.github\.io$/i.test(location.hostname);

    if (!canUsePhp && !FORMSUBMIT_ENDPOINT) {
      location.href = mailto;
      done.classList.add("is-visible");
      done.querySelector("[data-mail-note]").hidden = false;
      done.focus();
      return;
    }

    err.hidden = true;
    btn.disabled = true; btn.setAttribute("aria-busy", "true"); btn.textContent = "Bezig met versturen…";
    try {
      let result = canUsePhp ? await sendPhp().catch((x) => { if (!FORMSUBMIT_ENDPOINT || x.status === 429 || x.status === 403) throw x; return "unavailable"; }) : "unavailable";
      if (result === "unavailable") {
        if (!FORMSUBMIT_ENDPOINT) throw new Error("Geen verzendmethode beschikbaar");
        result = await sendFormSubmit();
      }
      if (result === "invalid") {
        btn.disabled = false; btn.removeAttribute("aria-busy"); btn.textContent = "Aanvraag versturen";
        form.querySelector('[aria-invalid="true"]')?.focus();
        return;
      }
      form.hidden = true; done.classList.add("is-visible"); done.focus();
      done.scrollIntoView({ block: "center" });
    } catch (x) {
      btn.disabled = false; btn.removeAttribute("aria-busy"); btn.textContent = "Aanvraag versturen";
      const mailLink = err.querySelector("a[data-mailto]");
      if (mailLink) mailLink.href = mailto;
      err.hidden = false; err.focus();
    }
  });
})();
