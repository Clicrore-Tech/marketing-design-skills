# Image prompting

Write prompts from the handoff spec, never from the user's one-line request.

## Prompt shape

```
<subject with specific details>, <action or pose>, <expression>,
<setting with 2 to 3 concrete props>, <time of day and light direction>,
<camera: lens feel, angle, depth of field>, <style: photographic / flat vector / 3D clay / ink illustration>,
<colour palette by role>, <empty space for text: where and how much>,
no text, no logos, no watermark
```

## Example (bakery launch, feed ad)

```
A smiling baker in her thirties with flour on her forearms,
lifting a tray of dark-crusted sourdough loaves out of a deck oven, looking at camera with quiet pride,
small artisan bakery with wooden shelves and linen proofing baskets out of focus behind,
early morning window light from the left with warm steam highlights,
85mm portrait lens feel, eye level, shallow depth of field,
photographic, natural skin texture,
warm cream and deep brown palette with a single mustard accent,
large empty area in the top third for a headline,
no text, no logos, no watermark
```

## Rules

- Generate without text, then set text in a layout tool. Image models still misspell, especially non-Latin scripts.
- Generate two or three variants per concept and choose on the phone preview.
- For real businesses, use real photos of real staff, customers (with consent), products and places. Use AI for backgrounds, objects, illustration and cleanup.
- Keep a real building or product recognisable if it appears. Do not invent a grander version.
- Save the final prompt in client memory so the look can be repeated.
