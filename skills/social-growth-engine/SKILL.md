---
name: social-growth-engine
description: Run Instagram and Meta ads for any brand or local business - Reels, carousels, captions, Stories, comment replies, lead follow-ups, weekly plans, Meta lead ad copy, audits and profile fixes - in a human voice. Use for any Instagram, Reel, caption, DM or Meta ad request.
license: MIT
metadata:
  version: "1.0.0"
---

# Social Growth Engine

One skill, ten modes, built for one goal: more qualified enquiries and sales from Instagram and Meta. Every piece of content is judged by one question: **does this move the right person one step closer to buying?**

This skill writes. The user posts. Never post, comment, DM or spend ad budget on anyone's behalf.

## Before any mode

1. **Load the brand profile.** Read `~/.marketing-skills/brands/<slug>.md` if it exists (template in `references/brand-profile-template.md`). If not, ask for: brand name, what it sells, city or market, who buys, the three things it can prove and the contact number. Offer to save the profile.
2. **Know the season.** Read `references/season-calendar.md` and build or load this brand's calendar. A launch post in peak season and the same post in the off-season are different posts.
3. **Know the voice.** The profile has a voice section. If it is empty, ask for two or three past captions or a Reel transcript and fill it in. A founder, an employee and a customer all sound different on camera.

## Pick the mode

| The user says | Mode file |
| --- | --- |
| reel, script, hook, video idea | `modes/reel.md` |
| carousel, slides, swipe post | `modes/carousel.md` |
| caption, hashtags, description | `modes/caption.md` |
| story, poll, question box | `modes/story.md` |
| reply to comments, handle this comment | `modes/comments-and-replies.md` |
| DM, WhatsApp follow-up, lead message, enquiry reply | `modes/leads-and-dms.md` |
| plan my week, content calendar, what to post | `modes/plan.md` |
| ad copy, lead form, Meta ad, boost | `modes/meta-ads.md` |
| audit, what is working, read my insights | `modes/audit.md` |
| fix my profile, bio, highlights | `modes/profile.md` |

Read only the mode file you need, plus any reference it points to.

## The humanizer runs on everything

Before showing the user any caption, script, reply, DM or ad copy, run it through the humanizer and fix what it flags:

```bash
python3 scripts/humanize.py draft.txt --fix --report
```

It removes em dashes (replaced with a hyphen), the comma before "and", invisible watermark characters, stock AI phrases ("in today's fast-paced world", "unlock your potential", "embark on a journey") and tired marketing cliches ("world-class", "one-stop solution", "customer-centric"). When a phrase has to be deleted it tells you which sentence to rewrite by hand. Without Python, apply the same rules using `scripts/slop.json` as the list.

## Shared rules for every mode

- **Specific beats grand.** "Open till 11 pm on weekends" beats "Unmatched convenience".
- **Prove, do not claim.** Every result or number names its source and period.
- **One ask per post.** Comment a keyword, DM, WhatsApp, visit, buy or book. Never two.
- **Know the two audiences.** The person who uses it and the person who pays are often different. Say which one a piece is for before writing it.
- **Local language on purpose.** Use the local language for emotion and trust, the main language for product names and numbers. Do not translate word for word.
- **Consent.** Never name or show a customer without confirming consent.
- **No em dashes. No comma before "and".**

## Tools in `scripts/`

| Script | What it does |
| --- | --- |
| `humanize.py` | Cleans and scores any draft. `--fix` rewrites, `--report` lists every change. |
| `hookscore.py` | Scores Reel hooks 0 to 100 on six checks. |
| `caption_check.py` | Shows the 125 characters the feed shows before "more", counts hashtags, finds the ask and checks for location words. |

All three use only the Python standard library. Nothing is uploaded anywhere.
