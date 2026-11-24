# Mode: Reel

Turn one true thing into a 15 to 45 second Reel that someone finishes.

## Get the raw material

A Reel needs one specific true thing. Ask one batched question if it is missing:
- What happened? (a result, a process, a customer story, a mistake, a question customers keep asking)
- Who is on camera? (founder, staff, customer, nobody with voiceover)
- What should the viewer do after? (comment a keyword, DM, WhatsApp, visit, buy)

## Write five hooks, score them, keep the best

Read `references/hooks.md`. Write five hooks from at least three different formulas. Save them one per line and run:

```bash
python3 scripts/hookscore.py hooks.txt
```

Keep the top scorer unless the user's gut says otherwise. A hook below 60 gets rewritten, not shot.

## Script shape

```
0-3s    HOOK      spoken line plus on-screen text (not identical to the spoken line)
3-8s    STAKE     why the viewer should care, one sentence
8-35s   PROOF     the demonstration, the story or the three steps, each beat under 5 seconds
last 5s ASK       one action, said out loud and shown on screen
```

Loop the ending back to the hook where possible. Second watches are free reach.

## Deliver

1. The hook, the spoken script with timecodes and the on-screen text per beat
2. A shot list the team can film on a phone in under 30 minutes
3. The caption (run `modes/caption.md`)
4. Audio suggestion: voice-led for trust content, trending audio only when it fits the audience
5. Cover frame text, six words or fewer

## Notes

- Real people on camera beat stock footage every time. Coach them: look at the lens, one take per beat.
- Show the real place and product. Customers compare the Reel with what they find when they arrive.
- Never script a customer to say something they would not say.
