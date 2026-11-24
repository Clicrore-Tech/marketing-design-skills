#!/usr/bin/env python3
"""Client memory: per-client brand facts, decisions, feedback and results.

    python3 client_memory.py init <slug> --name "Client name"
    python3 client_memory.py set <slug> brand.primary "#1B2A41"
    python3 client_memory.py log <slug> --kind decision --text "..." --tags launch,ad
    python3 client_memory.py show <slug>
    python3 client_memory.py search <slug> "red colour"
    python3 client_memory.py list

Stores JSON in $MARKETING_SKILLS_HOME/clients (default ~/.marketing-skills/clients). Standard library only.
"""
import argparse, datetime, json, os, re, sys
from pathlib import Path

ROOT = Path(os.environ.get("MARKETING_SKILLS_HOME", Path.home() / ".marketing-skills"))
CLIENTS = ROOT / "clients"
KINDS = ["decision", "feedback", "result", "brief", "asset", "note"]


def slug_ok(s):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", s):
        sys.exit("slug must be lowercase letters, digits and hyphens")
    return s


def path(slug):
    return CLIENTS / f"{slug_ok(slug)}.json"


def load(slug):
    p = path(slug)
    if not p.exists():
        sys.exit(f"No memory for '{slug}'. Run: client_memory.py init {slug} --name \"...\"")
    return json.loads(p.read_text(encoding="utf-8"))


def save(slug, data):
    CLIENTS.mkdir(parents=True, exist_ok=True)
    tmp = path(slug).with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path(slug))


def now():
    return datetime.datetime.now().isoformat(timespec="minutes")


def cmd_init(a):
    if path(a.slug).exists():
        sys.exit(f"'{a.slug}' already exists.")
    save(a.slug, {"slug": a.slug, "name": a.name, "created": now(), "brand": {}, "facts": {}, "log": []})
    profile = ROOT / "brands" / f"{a.slug}.md"
    print(f"Created {path(a.slug)}")
    if not profile.exists():
        print(f"Tip: also create the shared profile at {profile} from references/brand-profile-template.md")


def cmd_set(a):
    d = load(a.slug)
    keys = a.key.split(".")
    cur = d
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = a.value
    save(a.slug, d)
    print(f"{a.key} = {a.value}")


def cmd_log(a):
    d = load(a.slug)
    entry = {"at": now(), "kind": a.kind, "text": a.text, "tags": [t.strip() for t in a.tags.split(",") if t.strip()]}
    d["log"].append(entry)
    save(a.slug, d)
    print(f"Logged {a.kind}: {a.text}")


def show_entry(e):
    tags = f"  [{', '.join(e['tags'])}]" if e.get("tags") else ""
    print(f"  {e['at']}  {e['kind']:<9}{e['text']}{tags}")


def cmd_show(a):
    d = load(a.slug)
    print(f"{d['name']}  ({d['slug']})")
    for section in ("brand", "facts"):
        if d.get(section):
            print(section.upper())
            for k, v in d[section].items():
                print(f"  {k}: {v}")
    profile = ROOT / "brands" / f"{a.slug}.md"
    print(f"PROFILE  {profile if profile.exists() else 'none yet'}")
    for kind in KINDS:
        items = [e for e in d["log"] if e["kind"] == kind][-a.last:]
        if items:
            print(f"{kind.upper()} (latest {len(items)})")
            for e in items:
                show_entry(e)


def cmd_search(a):
    d = load(a.slug)
    terms = [t for t in re.findall(r"\w+", a.query.lower()) if len(t) > 2]
    scored = []
    for e in d["log"]:
        hay = (e["text"] + " " + " ".join(e.get("tags", []))).lower()
        s = sum(hay.count(t) for t in terms)
        if s:
            scored.append((s, e))
    for _, e in sorted(scored, key=lambda x: (-x[0], x[1]["at"]))[:a.limit]:
        show_entry(e)
    if not scored:
        print("No matches.")


def cmd_list(a):
    if not CLIENTS.exists():
        print("No clients yet.")
        return
    for p in sorted(CLIENTS.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        print(f"  {d['slug']:<28}{d['name']}  ({len(d['log'])} entries)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("slug"); p.add_argument("--name", required=True); p.set_defaults(f=cmd_init)
    p = sub.add_parser("set"); p.add_argument("slug"); p.add_argument("key"); p.add_argument("value"); p.set_defaults(f=cmd_set)
    p = sub.add_parser("log"); p.add_argument("slug"); p.add_argument("--kind", choices=KINDS, default="note"); p.add_argument("--text", required=True); p.add_argument("--tags", default=""); p.set_defaults(f=cmd_log)
    p = sub.add_parser("show"); p.add_argument("slug"); p.add_argument("--last", type=int, default=8); p.set_defaults(f=cmd_show)
    p = sub.add_parser("search"); p.add_argument("slug"); p.add_argument("query"); p.add_argument("--limit", type=int, default=10); p.set_defaults(f=cmd_search)
    p = sub.add_parser("list"); p.set_defaults(f=cmd_list)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
