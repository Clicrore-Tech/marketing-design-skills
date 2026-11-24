# Chart recipes for inline SVG

Every geometry value is computed from data. Write the maths as a comment above each chart so a reviewer can check it.

## Big number

```html
<div data-hero class="hero-num">38,000<span class="unit">classes booked</span></div>
```
Hero number at 18 to 26 percent of canvas width in font size. Unit at 25 percent of the number size.

## Pictogram army (customers, orders, members)

- Choose N per icon so the total icons land between 20 and 60.
- Grid columns = ceil(sqrt(icons x aspect)). Partial icon for the remainder: clip the last icon with a `clipPath` rect at `fraction x width`.
- Legend: "1 figure = N customers".

## Staircase trend (growth over time)

```
step_height_i = (value_i - floor) / (ceil - floor) * max_height
floor = min(values) - 5, ceil = 100 for percentages
```
Draw each year as a step block. Place a person or product figure on the top step. Label every step with the year and only the first and last with values, plus any dip.

## Tier ladder (packages or outcomes)

- Three rungs: highest, median and lowest (or count achieved).
- Rung y position proportional to value on a shared scale starting at 0.
- Median rung in the accent colour. Highest gets the label "Highest" and a smaller weight than you want to give it.

## Split bar against market average (prices)

```
bar_width = value / max(value, average) * track_width
```
Two bars on one track, brand on top. Difference labelled as a currency amount and a percent.

## Donut (part to whole, five slices max)

```
circumference = 2 * PI * r
dash_i = value_i / total * circumference
offset_i = -sum(dash_0 .. dash_{i-1})
```
Use `stroke-dasharray="dash_i circumference"` and `stroke-dashoffset="offset_i"`, rotate the group -90deg.

## Route timeline (process steps)

- A path with stations at equal arc lengths (`path.getTotalLength()` is not available at render time, so pre-compute with straight segments).
- Station labels alternate above and below to avoid collisions.
- The deadline station is the accent colour and slightly larger.

## Slot map (capacity left)

- Rows of chair icons, filled in `--muted` for taken, outlined in `--accent` for available.
- Only use when the number is real and current. Add "as on <date>".

## Number formatting

- Match the reader's locale: 1,25,000 and 1.2 Cr for Indian readers, 125,000 and 1.2M elsewhere.
- Percent with one decimal only when the decimal matters.
- Rankings with the source and year: "Rank 3, City Food Awards 2026".
