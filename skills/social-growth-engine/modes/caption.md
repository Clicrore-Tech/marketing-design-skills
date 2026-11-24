# Mode: Caption

## Decide the job first

**Reel caption:** the video already hooked them. The caption gives context, the one ask and the search words. Line one should not compete with the video.
**Image or carousel caption:** line one is the hook. Cut it at a cliff, not mid-sentence.

## Shape

```
LINE 1    the hook or the context, under 125 characters (what shows before "more")
BODY      2 to 5 short lines with specific details. A local-language line if bilingual.
ASK       one action: "Comment MENU and we will send this week's specials"
SEARCH    a line with the words people search: "<product> in <city>"
TAGS      3 to 5 hashtags, local plus specific
```

Then run:

```bash
python3 scripts/caption_check.py caption.txt --keywords "<product>" --city "<city>"
python3 scripts/humanize.py caption.txt --fix --report
```

Fix what they flag before showing the user.

## Rules

- Instagram search reads captions. Put the city and the product in plain words.
- Five specific hashtags beat thirty generic ones.
- Contact numbers go in the caption body, not only in the bio.
