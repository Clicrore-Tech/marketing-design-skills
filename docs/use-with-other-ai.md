# Using these skills outside Claude

The skills are written in the open Agent Skills format: a folder with a `SKILL.md` file, plus references and scripts. Claude, Codex and several other agents load them natively. Chat tools without skill support can still use them as custom instructions.

## Claude (claude.ai, Claude desktop, Cowork)

1. Zip one skill folder so the zip contains `ad-creative-director/SKILL.md` (the folder at the top, not loose files).
2. Open **Settings, Capabilities** and make sure code execution and skills are on.
3. Go to **Customize, Skills**, choose **Upload a skill** and pick the zip.
4. Start a new chat and ask for it by name.

## Claude Code

```bash
git clone https://github.com/Clicrore-Tech/marketing-design-skills.git
cd marketing-design-skills && ./install.sh
```

Or as a plugin:

```
/plugin marketplace add Clicrore-Tech/marketing-design-skills
/plugin install marketing-design-skills
```

## ChatGPT

**As a Custom GPT (best):**
1. Go to **Explore GPTs, Create**, then **Configure**.
2. Paste the body of one `SKILL.md` (everything below the `---` header) into **Instructions**.
3. Upload the files from that skill's `references/` (and `modes/` for the Instagram skill) under **Knowledge**.
4. Turn on **Code Interpreter** so the Python tools in `scripts/` can run. Upload the scripts as knowledge files and tell the GPT to run them.
5. Name it, for example "Ad Creative Director".

**In a ChatGPT Project:** add the `SKILL.md` text to the project instructions and upload the reference files to the project.

**Codex CLI:** run `./install.sh`. It installs into `~/.agents/skills`, which Codex reads. Invoke with `$ad-creative-director`.

## Grok

1. In grok.com, open **Projects** and create a project (for example "Social Growth Engine").
2. Paste the body of the `SKILL.md` into the project's custom instructions.
3. Attach the reference and mode files as project sources.
4. Grok cannot run the Python tools in every plan. When it cannot, ask it to apply the rules in `scripts/slop.json` by hand, or run the scripts yourself:

```bash
python3 scripts/humanize.py draft.txt --fix --report
```

## Gemini

Create a **Gem**: paste the `SKILL.md` body into the instructions and upload the reference files as knowledge. Gemini CLI users can run `./install.sh`, which copies the skills into `~/.gemini/skills` when that folder exists.

## What you lose without script support

| Skill | Without scripts |
| --- | --- |
| Infographic Studio | No automatic PNG render or overlap check. The AI writes the HTML and you open it in a browser and screenshot it. |
| Social Growth Engine | Hook scores, the humanizer and the caption check become manual checklists. |
| Ad Creative Director | Client memory becomes a pasted block of notes at the start of each chat. |
