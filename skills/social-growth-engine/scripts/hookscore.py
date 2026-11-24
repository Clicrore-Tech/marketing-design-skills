#!/usr/bin/env python3
"""Score Reel hooks, 0 to 100.

    python3 hookscore.py hooks.txt           # one hook per line, ranked
    python3 hookscore.py --hook "one line"

Six checks: FRONTLOAD, SPECIFICITY, AUDIENCE, TENSION, BREVITY, HONESTY.
Heuristic, not a prediction. Use it to compare options, then trust the account's own data.
"""
import argparse, re
from pathlib import Path

DEALBREAKERS = [
    (r"^(hi|hello|hey|namaskara|good (morning|evening))\b", "Greeting. Nobody came to the feed to be greeted."),
    (r"^(welcome to|presenting|introducing)\b", "Opens with a welcome. Start with the point."),
    (r"\bstop scrolling\b", "Asking for attention proves you have not earned it."),
    (r"^(\d+ ?% off|sale|offer|discount)\b", "The offer is the ask, not the hook."),
    (r"\b(best|no\.? ?1|number one|top)\b \w+ (in|of) (town|the city|india|the world)\b", "Unprovable superlative without a source."),
    (r"\bguarantee", "Guarantees you cannot honour break advertising rules."),
]
AUDIENCE = r"\b(you|your|yours|everyone|anyone|beginners?|owners?|founders?|parents?|moms?|dads?|brides?|runners?|customers?|buyers?|people)\b"
TENSION = r"\b(mistake|wrong|myth|truth|nobody|never|secret|why|how|really|actually|vs|before|after|left|only|stop|cost)\b|\?"
CONCRETE = r"\d|\b(price|cost|rupees?|rs|km|kg|minutes?|hours?|days?|weeks?|am|pm|recipe|route|clause|menu|order|client|customer|mistake)\b"


def score(h):
    low = h.lower().strip()
    words = low.split()
    first4 = " ".join(words[:4])
    checks = {}
    checks["FRONTLOAD"] = 100 if re.search(CONCRETE + "|" + TENSION, first4) else 60 if re.search(AUDIENCE, first4) else 20
    n = len(re.findall(CONCRETE, low))
    checks["SPECIFICITY"] = min(100, 30 + 35 * n)
    checks["AUDIENCE"] = 100 if re.search(AUDIENCE, low) else 40
    checks["TENSION"] = min(100, 30 + 35 * len(re.findall(TENSION, low)))
    wc = len(words)
    checks["BREVITY"] = 100 if 5 <= wc <= 14 else 70 if wc <= 18 else 40 if wc <= 24 else 10
    checks["HONESTY"] = 100
    deal = [msg for pat, msg in DEALBREAKERS if re.search(pat, low)]
    if deal:
        checks["HONESTY"] = 20
    weights = {"FRONTLOAD": .25, "SPECIFICITY": .2, "AUDIENCE": .15, "TENSION": .2, "BREVITY": .1, "HONESTY": .1}
    total = sum(checks[k] * w for k, w in weights.items())
    if deal:
        total = min(total, 45)
    return round(total, 1), checks, deal


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--hook")
    a = ap.parse_args()
    hooks = [a.hook] if a.hook else [l.strip() for l in Path(a.file).read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = sorted(((score(h), h) for h in hooks), key=lambda x: -x[0][0])
    print("HOOK RANKING")
    print("=" * 78)
    for i, ((t, checks, deal), h) in enumerate(rows):
        tag = "STRONG" if t >= 75 else "OK" if t >= 60 else "WEAK"
        weakest = min(checks, key=checks.get)
        print(f"{'->' if i == 0 else '  '} {t:5.1f} {tag:<7}{h[:62]}{'...' if len(h) > 62 else ''}")
        print(f"         weakest: {weakest} ({checks[weakest]})")
        for d in deal:
            print(f"         dealbreaker: {d}")


if __name__ == "__main__":
    main()
