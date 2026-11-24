#!/usr/bin/env node
// Render an infographic HTML file to PNG, or to MP4/GIF when --video <seconds> is given.
//
//   node scripts/render.mjs post.html post.png --preset feed [--scale 2]
//   node scripts/render.mjs post.html post.mp4 --preset story --video 8 [--fps 30]
//
// Video mode captures frames by pausing CSS animations at each timestamp, then
// stitches them with ffmpeg (must be on PATH).

import { chromium } from 'playwright';
import { pathToFileURL } from 'node:url';
import { resolve, extname, join } from 'node:path';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { spawnSync } from 'node:child_process';
import { PRESETS, parseArgs } from './presets.mjs';

let args;
try { args = parseArgs(process.argv.slice(2)); } catch (e) { console.error(e.message); process.exit(1); }
const [input, output] = args.positional;
if (!input || !output) {
  console.error('Usage: node scripts/render.mjs input.html output.(png|mp4|gif) [--preset feed|square|story|ad-link|a4|flex] [--scale N] [--video seconds] [--fps N]');
  process.exit(1);
}
const { width, height } = PRESETS[args.preset];
const isVideo = ['.mp4', '.gif'].includes(extname(output).toLowerCase());
if (isVideo && !args.video) { console.error('Give --video <seconds> for MP4 or GIF output.'); process.exit(1); }

const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: isVideo ? 1 : args.scale });
  await page.goto(pathToFileURL(resolve(input)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  if (!isVideo) {
    // Jump every animation to its end state so the still matches the final frame.
    await page.evaluate(() => document.getAnimations().forEach(a => { try { a.finish(); } catch {} }));
    await page.screenshot({ path: output, clip: { x: 0, y: 0, width, height } });
    console.log(`Rendered ${output} at ${width * args.scale}x${height * args.scale}`);
  } else {
    const fps = args.fps || 30;
    const frames = Math.round(args.video * fps);
    const dir = mkdtempSync(join(tmpdir(), 'infographic-frames-'));
    await page.evaluate(() => document.getAnimations().forEach(a => a.pause()));
    for (let i = 0; i < frames; i++) {
      const t = (i / fps) * 1000;
      await page.evaluate(ms => document.getAnimations().forEach(a => { a.currentTime = ms; }), t);
      await page.screenshot({ path: join(dir, `f${String(i).padStart(5, '0')}.png`), clip: { x: 0, y: 0, width, height } });
    }
    const gif = extname(output).toLowerCase() === '.gif';
    const ff = gif
      ? ['-y', '-framerate', String(fps), '-i', join(dir, 'f%05d.png'), '-vf', `fps=15,scale=${Math.min(width, 720)}:-1:flags=lanczos`, output]
      : ['-y', '-framerate', String(fps), '-i', join(dir, 'f%05d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', output];
    const r = spawnSync('ffmpeg', ff, { stdio: 'inherit' });
    rmSync(dir, { recursive: true, force: true });
    if (r.status !== 0) { console.error('ffmpeg failed. Is it installed? (brew install ffmpeg)'); process.exit(1); }
    console.log(`Rendered ${output}: ${frames} frames at ${fps} fps`);
  }
} finally {
  await browser.close();
}
