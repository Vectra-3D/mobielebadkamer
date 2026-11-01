---
name: Mobiele Badkamer
description: Tijdelijke badkamer op je oprit — douche, toilet, wastafel, verwarmd.
colors:
  blue: "oklch(0.50 0.15 253)"
  blue-deep: "oklch(0.40 0.13 256)"
  ink: "oklch(0.24 0.055 258)"
  ink-soft: "oklch(0.42 0.035 256)"
  tile: "oklch(0.975 0.008 250)"
  grout: "oklch(0.90 0.018 250)"
  surface: "oklch(1 0 0)"
  red: "oklch(0.55 0.205 27)"
  red-deep: "oklch(0.47 0.18 27)"
  sun: "oklch(0.90 0.13 95)"
typography:
  display:
    fontFamily: "Bricolage Grotesque, system-ui, sans-serif"
    fontSize: "clamp(2.4rem, 5.5vw + 0.5rem, 4.75rem)"
    fontWeight: 720
    lineHeight: 1
    letterSpacing: "-0.03em"
  body:
    fontFamily: "Atkinson Hyperlegible Next, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
rounded:
  sm: "6px"
  md: "12px"
  lg: "20px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "48px"
  xl: "clamp(64px, 9vw, 128px)"
components:
  button-primary:
    backgroundColor: "{colors.red}"
    textColor: "{colors.surface}"
    rounded: "{rounded.sm}"
    padding: "14px 22px"
  button-primary-hover:
    backgroundColor: "{colors.red-deep}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
---

## Overview
Practical, reassuring, local. The site is built around the real trailer and real numbers. The signature motif is the **bathroom tile**: a quiet 1px grout grid on tinted sections, square photo crops, and a price "tag" that sits on the hero photo like a sticker on the unit itself.

## Colors
Committed strategy: the logo's blue carries the hero and the closing band (drenched), white/tile sections carry content. The logo's red is the action colour (primary buttons, the price tag) and is used for nothing decorative. Sun yellow is a one-off highlight for availability/ticks on blue only.

## Typography
Bricolage Grotesque (display, variable opsz/wdth) for headings and prices: sturdy, a little quirky, like hand-painted trailer lettering. Atkinson Hyperlegible Next for body: built for legibility, fits the older audience. Prices use tabular numerals.

## Elevation
Mostly flat. One shadow token for floating things (sticky mobile bar, price tag, dialogs): `0 1px 2px oklch(0.24 0.05 258 / .08), 0 12px 32px -12px oklch(0.24 0.05 258 / .28)`.

## Components
Buttons (primary red, secondary white outline, ghost-on-blue), price tag, product chooser (two asymmetric panels), unit floor-plan (SVG with numbered hotspots), step sequence (the one place numbers are used), spec table, FAQ (native details/summary), gallery with dialog lightbox, request form with live price estimate, sticky mobile call/request bar.

## Do's and Don'ts
- Do show price with btw status every time.
- Do use the real photos; never stock bathrooms.
- Don't put eyebrow labels above headings; headings carry themselves.
- Don't use red for decoration or errors-only; errors use red + icon + text.
- Don't animate content into visibility; motion only enhances what's already shown.
