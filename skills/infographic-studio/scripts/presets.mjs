// Canvas presets shared by render.mjs and check.mjs.
export const PRESETS = {
  feed: { width: 1080, height: 1350, ad: true },
  square: { width: 1080, height: 1080, ad: true },
  story: { width: 1080, height: 1920, ad: true, safeTop: 250, safeBottom: 340 },
  'ad-link': { width: 1200, height: 628, ad: true },
  a4: { width: 1240, height: 1754 },
  flex: { width: 1800, height: 900 },
};

// Smallest readable font size in CSS px for each canvas, judged at phone size.
export const FONT_FLOOR = { feed: 18, square: 18, story: 20, 'ad-link': 16, a4: 14, flex: 28 };

export function parseArgs(argv, extra = {}) {
  const args = { preset: 'feed', scale: 2, ...extra };
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--preset') args.preset = argv[++i];
    else if (a === '--scale') args.scale = Number(argv[++i]);
    else if (a === '--video') args.video = Number(argv[++i]);
    else if (a === '--fps') args.fps = Number(argv[++i]);
    else if (a.startsWith('--')) throw new Error(`Unknown flag ${a}`);
    else positional.push(a);
  }
  args.positional = positional;
  if (!PRESETS[args.preset]) throw new Error(`Unknown preset "${args.preset}". Use one of: ${Object.keys(PRESETS).join(', ')}`);
  return args;
}
