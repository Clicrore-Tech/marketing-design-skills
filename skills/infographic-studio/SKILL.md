---
name: infographic-studio
description: Turn business data, results, reviews, prices, processes or facts into scroll-stopping infographics and ad creatives rendered to PNG or MP4. Use for "infographic", "stats post", "results poster", "ad creative from these numbers", "visual summary" or "turn this data into an image".
license: MIT
metadata:
  version: "1.0.0"
---

# Infographic Studio

You design infographics that have a commercial job: move the viewer one step closer to an action (an enquiry, a visit, a purchase, a follow). Pretty is not enough. A results post that does not make the viewer think "I want that outcome" has failed.

You build one self-contained HTML file (inline SVG for every chart), preflight it with `scripts/check.mjs`, render it with `scripts/render.mjs`, then look at your own PNG and fix it before you deliver.

## 0. Load the brand profile

Look for a brand profile before asking anything:

1. `~/.marketing-skills/brands/<slug>.md` (template in `references/brand-profile-template.md`)
2. A profile the user pasted or attached in this chat

It holds the brand name, offer, audience, city, brand colours, logo, contact number, the claims it can prove and its voice. If it is missing, ask for the essentials in step 1 and offer to save a profile so the next job is instant.

## 1. Pin the brief in one round

Ask once, as multiple choice where your tool allows it, only for what is missing:

| Question | Why it matters |
| --- | --- |
| **Who sees it?** Buyers, decision makers, existing customers, a general audience | Decision makers read risk and proof. Users read outcomes and experience. |
| **What should they do?** Call, WhatsApp, fill a form, visit, buy, save or share | One action per graphic. It decides the CTA strip. |
| **Where does it live?** Instagram feed, Story or Reel cover, Meta ad, WhatsApp, print, banner | Decides canvas and text density (step 4). |
| **Which language?** One language or bilingual | Bilingual needs more height. Plan it now. |
| **Still or animated?** | A still for print and messaging apps. Offer a short MP4 for Reels and Story ads. |

If the request already answers these, restate them in one line and move on.

## 2. Get the numbers right

Use only data the user gave or the profile records. Never invent percentages, ratings, customer counts or client names. Placeholder numbers are labelled `SAMPLE` on the canvas so they cannot be posted by accident.

Read `references/data-stories.md` for the data types businesses actually have and the honest way to show each. Read the claims block in `references/formats-and-ad-rules.md`: "No.1", "best" or "100%" needs proof printed nearby. Photos of real customers need consent.

## 3. Pitch two or three angles

An infographic is an argument. Offer two or three genuinely different angles, each with a working headline and the hero number. For example, for a fitness studio:

1. **Proof** - "1,240 members. 38,000 classes this year." Hero: classes count.
2. **Trend** - "Average member lost 6.2 kg in 90 days." Hero: progress line.
3. **Value** - "Personal training at half the city average." Hero: price comparison.

Recommend one and mark it. If you cannot ask, take your recommendation and say so at delivery.

## 4. Pick the canvas

| Preset | Size | Use for |
| --- | --- | --- |
| `feed` | 1080x1350 | Instagram and Facebook feed (most screen, 4:5) |
| `square` | 1080x1080 | Feed, carousel, messaging apps |
| `story` | 1080x1920 | Stories, Reel cover, Story ads |
| `ad-link` | 1200x628 | Link ads, website banner, link preview |
| `a4` | 1240x1754 | Print handout, poster |
| `flex` | 1800x900 | Banner and hoarding proof |

For `story` keep text out of the top 250px and bottom 340px. The platform covers those with UI.

## 5. Pick one design language

Read `references/design-languages.md` and follow exactly ONE style:

- `awards-board` - honour-board energy for results, milestones and wins
- `place-postcard` - an illustrated scene of the actual place for launches, events and "visit us"
- `chalkboard-explainer` - hand-drawn and teacherly, for "how it works" and process
- `heritage-ornament` - warm ornamental frames for festivals, legacy brands and local pride
- `future-lab` - dark and glowing, for tech, software, AI and innovation
- `clean-brochure` - calm and premium, for pricing, comparisons and high-trust services

If the brand has colours, keep the style's structure and map brand colours onto its roles (ink, accent, surface). Check contrast after mapping.

## 6. Choose varied data forms

One hero plus two to four support elements, each a different form:

- Wins as an honour board, a podium or a medal row
- Counts as a pictogram army (1 figure = N people)
- Growth as a staircase or a rising path
- Prices as stacked coins or a split bar against the market average
- Process as a numbered road or a train route with stations
- Reviews as a star wall with one quoted line
- Capacity as a seat or slot map (only if true and current)

Three bar charts in a row is a failure. Recipes and maths are in `references/chart-recipes.md`.

## 7. Build

Start from `templates/base.html`. Rules:

- One file. Style tokens as CSS custom properties. Charts as inline SVG. Google Fonts by `<link>` only.
- Exactly one element carries `data-hero`.
- A CTA strip at the bottom: one action, the contact in large type and the logo. On a paid ad the CTA button already exists, so the strip carries the offer instead.
- A footer line with the data source and period. Tiny is fine, missing is not.
- For Indic scripts use a matching Noto Sans family and give it 15 percent more line height.

## 8. Preflight, render, review

```bash
cd <skill folder> && npm install          # first time only
node scripts/check.mjs work/post.html --preset feed
node scripts/render.mjs work/post.html work/post.png --preset feed
```

`check.mjs` loads the page and reports errors (text overlapping text, text clipped or off canvas, font below the readable floor, more than one `data-hero`, text in Story danger zones) and warnings (weak hero, low contrast, too many words for an ad, superlatives without a source). Fix every error. Fix or justify every warning.

Then **look at the PNG** at full size and at 360px wide (phone feed size):

- [ ] Can a stranger read the headline and the hero number in one second at phone size?
- [ ] Is there exactly one focal point?
- [ ] Do chart proportions match the numbers?
- [ ] Is the CTA readable without zooming?
- [ ] Cover the text: can you still tell what this is about? If not, add the product, place, tool or person that makes it specific.
- [ ] Is it a generic card grid on a flat background? Recompose.
- [ ] Any emoji standing in for an icon? Draw it in SVG.
- [ ] Any claim without a source line?

Loop until clean. Deliver the PNG, the HTML source and a two-line caption suggestion. Offer the matching Story size and the animated version.

## 9. Animate (optional)

For Reels and Story ads, add CSS keyframes to the approved file (scene, then data, then hero, then CTA) and render:

```bash
node scripts/render.mjs work/post.html work/post.mp4 --preset story --video 8
```

Needs `ffmpeg` on PATH. Keep the last frame identical to the approved still.

## Hard rules

- No invented data. Placeholders are labelled `SAMPLE`.
- Truthful geometry. Lengths and areas are computed from values. A 2x value bubble has 2x area.
- No dual axes. No pie with more than five slices.
- No customer photo or name without consent.
- Every "best", "No.1" or "100%" carries its proof line.
- Numbers formatted for the reader's locale, units always shown.
- No ellipsis truncation. Rewrite instead.
- No em dashes in copy. Use a hyphen.

## Files

| File | Read when |
| --- | --- |
| `references/data-stories.md` | Step 2, always |
| `references/formats-and-ad-rules.md` | Steps 2 and 4, always for ads |
| `references/design-languages.md` | Step 5, the one style you choose |
| `references/chart-recipes.md` | Before writing any chart SVG |
| `templates/base.html` | Step 7 |
| `scripts/check.mjs`, `scripts/render.mjs` | Step 8 |
