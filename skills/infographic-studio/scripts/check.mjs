#!/usr/bin/env node
// Preflight an infographic before rendering. Measures real glyph boxes in Chromium.
//
//   node scripts/check.mjs post.html --preset feed
//
// Errors (exit code 1): text overlapping other text, text clipped or off canvas,
// font below the readable floor, more than one data-hero, text in story danger zones.
// Warnings: missing or weak hero, low contrast, too many words for an ad canvas,
// "best / No.1 / 100%" claims without a visible source line.

import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';
import { PRESETS, FONT_FLOOR, parseArgs } from './presets.mjs';

let args;
try { args = parseArgs(process.argv.slice(2)); } catch (e) { console.error(e.message); process.exit(1); }
const [input] = args.positional;
if (!input) { console.error('Usage: node scripts/check.mjs input.html [--preset name]'); process.exit(1); }
const preset = PRESETS[args.preset];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: preset.width, height: preset.height } });
await page.goto(pathToFileURL(resolve(input)).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => document.getAnimations().forEach(a => { try { a.finish(); } catch {} }));

const report = await page.evaluate(({ preset, floor }) => {
  const errors = [], warnings = [];
  const W = preset.width, H = preset.height;

  // Collect one box per text run (text nodes measured through Range).
  const runs = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const text = node.textContent.trim();
    if (!text) continue;
    const el = node.parentElement;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || Number(cs.opacity) === 0) continue;
    const range = document.createRange();
    range.selectNodeContents(node);
    for (const r of range.getClientRects()) {
      if (r.width < 1 || r.height < 1) continue;
      runs.push({ el, text: text.slice(0, 40), x: r.left, y: r.top, w: r.width, h: r.height, size: parseFloat(cs.fontSize), color: cs.color });
    }
  }
  const label = r => `"${r.text}"`;

  // Off canvas and clipped by an overflow ancestor.
  for (const r of runs) {
    if (r.x < -1 || r.y < -1 || r.x + r.w > W + 1 || r.y + r.h > H + 1) errors.push(`${label(r)} runs off the canvas`);
    let a = r.el.parentElement;
    while (a && a !== document.body) {
      const cs = getComputedStyle(a);
      if (/(hidden|clip)/.test(cs.overflow + cs.overflowX + cs.overflowY)) {
        const b = a.getBoundingClientRect();
        if (r.x < b.left - 1 || r.y < b.top - 1 || r.x + r.w > b.right + 1 || r.y + r.h > b.bottom + 1) { errors.push(`${label(r)} is clipped by its container`); break; }
      }
      a = a.parentElement;
    }
    if (r.size < floor) errors.push(`${label(r)} is ${r.size}px, below the ${floor}px floor for this canvas`);
    if (preset.safeTop && (r.y < preset.safeTop || r.y + r.h > H - preset.safeBottom)) errors.push(`${label(r)} sits in the Story UI danger zone`);
  }

  // Text over text.
  const ok = el => el.closest('[data-overlap-ok]');
  for (let i = 0; i < runs.length; i++) for (let j = i + 1; j < runs.length; j++) {
    const a = runs[i], b = runs[j];
    if (a.el === b.el || a.el.contains(b.el) || b.el.contains(a.el) || ok(a.el) || ok(b.el)) continue;
    // Range boxes include the font's full ascent and descent, which is taller than
    // the visible ink for big display type. Trim to an approximate ink box first.
    const ink = r => { const t = Math.max(0, (r.h - r.size) / 2) + r.size * 0.12; return { y: r.y + t, h: Math.max(1, r.h - 2 * t) }; };
    const ia = ink(a), ib = ink(b);
    const ox = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
    const oy = Math.min(ia.y + ia.h, ib.y + ib.h) - Math.max(ia.y, ib.y);
    if (ox > 2 && oy > 2) errors.push(`${label(a)} overlaps ${label(b)}`);
  }

  // Hero.
  const heroes = document.querySelectorAll('[data-hero]');
  if (heroes.length > 1) errors.push(`${heroes.length} elements carry data-hero. Pick one.`);
  if (heroes.length === 0) warnings.push('No data-hero. Mark the one element that should win the squint test.');
  if (heroes.length === 1) {
    const heroSize = parseFloat(getComputedStyle(heroes[0]).fontSize) || 0;
    const others = runs.filter(r => !heroes[0].contains(r.el)).map(r => r.size);
    const maxOther = Math.max(0, ...others);
    if (heroSize && heroSize < maxOther * 1.6) warnings.push(`Hero is ${heroSize}px but another text is ${maxOther}px. Make the hero at least 1.6x bigger.`);
  }

  // Contrast against the nearest solid background.
  const lum = c => { const m = c.match(/\d+(\.\d+)?/g).map(Number); const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(m[0]) + 0.7152 * f(m[1]) + 0.0722 * f(m[2]); };
  const bgOf = el => { while (el) { const c = getComputedStyle(el).backgroundColor; const m = c.match(/[\d.]+/g); if (m && (m.length < 4 || Number(m[3]) > 0.9)) return c; el = el.parentElement; } return null; };
  for (const r of runs) {
    const bg = bgOf(r.el); if (!bg) continue;
    const [l1, l2] = [lum(r.color), lum(bg)].sort((a, b) => b - a);
    const ratio = (l1 + 0.05) / (l2 + 0.05);
    const need = r.size >= 32 ? 3 : 4.5;
    if (ratio < need) warnings.push(`${label(r)} contrast ${ratio.toFixed(1)}:1, needs ${need}:1`);
  }

  // Ad word count and unsupported claims.
  const words = document.body.innerText.split(/\s+/).filter(Boolean).length;
  if (preset.ad && words > 35) warnings.push(`${words} words on an ad canvas. Aim for 35 or fewer, move the rest to the caption.`);
  const txt = document.body.innerText;
  if (/\b(best|no\.?\s?1|number one|100\s?%|guarantee)/i.test(txt) && !/source|as per|ranked by|batch/i.test(txt)) warnings.push('Superlative or 100% claim with no visible source line. See formats-and-meta-rules.md.');
  if (/[\u2014]/.test(txt)) warnings.push('Em dash found in copy. Use a hyphen.');

  return { errors: [...new Set(errors)], warnings: [...new Set(warnings)], runs: runs.length };
}, { preset, floor: FONT_FLOOR[args.preset] });

await browser.close();
console.log(`CHECK ${input}  preset=${args.preset}  text runs=${report.runs}`);
for (const e of report.errors) console.log(`  ERROR    ${e}`);
for (const w of report.warnings) console.log(`  warning  ${w}`);
console.log(`${report.errors.length} errors, ${report.warnings.length} warnings`);
process.exit(report.errors.length ? 1 : 0);
