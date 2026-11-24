# Formats, ad placement rules and claims

## Canvas presets

| Preset | Pixels | Placement | Notes |
| --- | --- | --- | --- |
| `feed` | 1080x1350 | Instagram and Facebook feed, feed ads | Most screen space. Default for ads. |
| `square` | 1080x1080 | Feed, carousel cards, messaging apps | Safe everywhere. |
| `story` | 1080x1920 | Stories, Reel cover, Story and Reel ads | Keep text out of the top 250px and bottom 340px. |
| `ad-link` | 1200x628 | Link ads, website hero, link preview | Headline plus one number only. |
| `a4` | 1240x1754 | Print | Render with `--scale 2.5` for about 300 dpi. |
| `flex` | 1800x900 | Banner proofs | Headline at least 120px to read from 10 metres. |

## Text on ad images

Ad platforms no longer reject images for text, but delivery usually costs more when an image is mostly words. Aim for headline plus hero number plus one supporting line. Everything else goes in the ad copy. `check.mjs` warns above 35 words on an ad canvas.

## Safe zones

- **Story and Reel**: top 14 percent holds the profile row, bottom 18 percent holds the CTA and caption.
- **Feed 4:5**: the profile grid crops to 3:4. Keep the headline inside the central 1012px.
- **Carousel**: card one must work alone in the feed.

## Claims (general advertising practice)

Most advertising standards bodies (ASCI in India, ASA in the UK, the FTC in the US) share the same core rules. This is a working summary, not legal advice.

1. **Substantiate** every objective claim. Results, ratings and numbers name their source and period.
2. **Superlatives** like "best" or "No.1" need verifiable third-party evidence shown with the claim.
3. **Testimonials** must be real, current and from real customers who agreed to be featured.
4. **Typical results** must be shown when you feature an exceptional one.
5. **No guarantees** you cannot honour.
6. **Prices** must not hide mandatory charges.

When a claim fails a rule, do not drop it silently. Tell the user which rule it fails and offer compliant wording.

## Platform policy reminders

- Do not assert personal attributes in ad copy ("Are you overweight?" is out; "Ready for a stronger 2027?" is fine).
- Before and after images need real, consented data and must not imply guaranteed results.
- Photos of minors need guardian consent.
