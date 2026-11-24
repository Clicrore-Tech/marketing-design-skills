# Client memory

An agency works with many clients. Each gets a private memory file so the next job starts where the last one ended.

## Where it lives

- `~/.marketing-skills/clients/<slug>.json` - brand, assets, decisions, feedback, results (managed by `scripts/client_memory.py`)
- `~/.marketing-skills/brands/<slug>.md` - the shared brand profile read by all three skills

Set `MARKETING_SKILLS_HOME` to move the root (for example to a synced Google Drive folder).

## Commands

```bash
python3 scripts/client_memory.py init <slug> --name "Crust Bakery"
python3 scripts/client_memory.py set <slug> brand.primary "#1B2A41"
python3 scripts/client_memory.py set <slug> brand.logo "~/Clients/crust/logo.png"
python3 scripts/client_memory.py log <slug> --kind decision|feedback|result|brief|asset --text "..." --tags a,b
python3 scripts/client_memory.py show <slug>
python3 scripts/client_memory.py search <slug> "colour red"
python3 scripts/client_memory.py list
```

## What to save

- Brand facts the client confirmed
- Every approved creative and its concept name
- Every rejection and the reason
- Real results: CTR, cost per lead, qualified leads, which creative
- Prompts that produced an approved image

## What never to save

- Passwords, ad account tokens or payment details
- Customer personal data beyond what the client approved for a specific creative
