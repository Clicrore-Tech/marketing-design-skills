# Six design languages

Read only the style you chose. Its tokens are the law for that graphic. If the brand has colours, keep the structure and map brand colours onto the roles, then check contrast (body text at least 4.5:1, large text at least 3:1).

Every style has a scene. A flat background with cards is not a style.

---

## awards-board

**Use for:** results, milestones, rankings, wins, "year in numbers".
**Scene:** a polished wooden honour board under a spotlight, gold lettering, name plates.

| Role | Token | Value |
| --- | --- | --- |
| Surface | `--bg` | `#1B2A41` with a radial spotlight to `#2E4670` |
| Board | `--board` | `#5A3A22` walnut with a `#C9A227` gold inlay border |
| Ink | `--ink` | `#F7F3E8` |
| Muted | `--muted` | `#B9C2D3` |
| Accent | `--accent` | `#E8B931` |
| Data slots | `--d1..d4` | `#E8B931`, `#7FB7E6`, `#E37A5B`, `#9CCB8A` |

**Type:** headlines `Cinzel` 700, numbers `Oswald` 600, body `Inter`.
**Signature devices:** engraved name plates, a crest tab on the board, a laurel SVG around the hero number, a spotlight beam.
**Do not:** more than eight plates on one canvas. Clip-art trophies. Glitter.

---

## place-postcard

**Use for:** launches, events, openings, "visit us", tours.
**Scene:** an illustrated postcard of the actual place in flat-shaded vector, people arriving, a sky band that shows the season.

| Role | Token | Value |
| --- | --- | --- |
| Sky | `--sky` | `#BFE3F2` to `#FDF6E3` |
| Ground | `--ground` | `#6BA368` |
| Building | `--build` | `#F2D7B6` with `#C8875A` roof |
| Ink | `--ink` | `#1E2B33` |
| Accent | `--accent` | `#E2572C` |
| Data slots | `--d1..d4` | `#E2572C`, `#2E86AB`, `#F2A541`, `#5C946E` |

**Type:** headlines `Baloo 2` 800, body `Nunito` 500.
**Signature devices:** a postage stamp holding the date, a dashed path leading to the door where the CTA sits, numbered pins on the building.
**Do:** draw the real building silhouette from a photo. **Do not:** paste stock cutouts on the illustration.

---

## chalkboard-explainer

**Use for:** process explainers, "how it works", tips, comparisons.
**Scene:** a green slate with a wooden frame, chalk dust, a duster on the ledge.

| Role | Token | Value |
| --- | --- | --- |
| Slate | `--bg` | `#2F4F3E` with a subtle noise texture |
| Frame | `--frame` | `#8A5A2B` |
| Chalk | `--ink` | `#F4F1E8` |
| Muted | `--muted` | `#B8C7B9` |
| Accent | `--accent` | `#F6D365` |
| Data slots | `--d1..d4` | `#F6D365`, `#F49BA6`, `#9AD0EC`, `#C5E59C` |

**Type:** headlines `Kalam` 700 or `Caveat Brush`, body `Kalam`.
**Signature devices:** hand-drawn arrows, circled numbers, underline swashes, a sticky note for the CTA.
**Do not:** long paragraphs in chalk fonts. Max 12 words per block.

---

## heritage-ornament

**Use for:** festivals, legacy brands, local pride, greetings with a soft offer.
**Scene:** an arched ornamental frame with a mandala border, warm sandstone, a woven textile band.

| Role | Token | Value |
| --- | --- | --- |
| Sandstone | `--bg` | `#F5E6CC` |
| Maroon | `--ink` | `#5B1A18` |
| Gold | `--accent` | `#C99A2E` |
| Muted | `--muted` | `#8C6A52` |
| Band | `--band` | `#7A1F3D` with `#1F6F5C` border |
| Data slots | `--d1..d4` | `#7A1F3D`, `#1F6F5C`, `#C99A2E`, `#D9733B` |

**Type:** headlines `Yatra One` or `Rozha One`, body `Mukta` 500.
**Signature devices:** a scalloped arch around the hero, a lamp or bell motif in SVG, a patterned strip along the base holding the CTA.
**Do:** ornament on the frame, data in clean space. **Do not:** use landmark photos you have no rights to.

---

## future-lab

**Use for:** tech, software, AI, engineering, innovation, product launches.
**Scene:** a dark lab with a glowing circuit floor and holographic panels.

| Role | Token | Value |
| --- | --- | --- |
| Background | `--bg` | `#0B1020` with a `#1A2350` radial glow |
| Panel | `--panel` | `rgba(120,160,255,0.08)` with a 1px `rgba(140,180,255,0.35)` border |
| Ink | `--ink` | `#EAF0FF` |
| Muted | `--muted` | `#93A1C8` |
| Accent | `--accent` | `#38E1C6` |
| Data slots | `--d1..d4` | `#38E1C6`, `#7C83FD`, `#FFB86B`, `#FF6B9A` |

**Type:** headlines `Space Grotesk` 700, numbers `JetBrains Mono` 600, body `Inter`.
**Signature devices:** circuit traces that carry data (trace length = value), a terminal window for the CTA, glow only on the hero.
**Do not:** purple gradients everywhere. Binary rain. Robot hand touching a human hand.

---

## clean-brochure

**Use for:** pricing, packages, comparisons, premium and high-trust services.
**Scene:** an open printed brochure on a desk in soft daylight, paper texture, a pen.

| Role | Token | Value |
| --- | --- | --- |
| Paper | `--bg` | `#FBFAF7` |
| Ink | `--ink` | `#1C2430` |
| Muted | `--muted` | `#6B7684` |
| Accent | `--accent` | brand colour, else `#0F6E7A` |
| Rule | `--rule` | `#E3E0D8` |
| Data slots | `--d1..d4` | `#0F6E7A`, `#C8693D`, `#6A7FDB`, `#9DA84A` |

**Type:** headlines `Fraunces` 600, body `Source Sans 3`.
**Signature devices:** a page-fold shadow, a margin note in the accent colour, a ribbon bookmark holding the CTA.
**Do not:** turn it into a card grid. It is a page, not a dashboard.
