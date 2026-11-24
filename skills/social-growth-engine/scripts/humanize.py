#!/usr/bin/env python3
"""Humanizer: strip the AI fingerprint from a draft and score it.

    python3 humanize.py draft.txt                 # score only
    python3 humanize.py draft.txt --fix --report  # rewrite in place and list changes
    python3 humanize.py draft.txt --fix --out clean.txt
    echo "text" | python3 humanize.py -           # read stdin

Style enforced: no em dashes (hyphen instead) and no comma before "and".
Standard library only. Nothing leaves the machine.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEX = json.loads((HERE / "slop.json").read_text(encoding="utf-8"))


def clean(text):
    changes = []
    for ch in LEX["invisible"]:
        n = text.count(ch)
        if n:
            text = text.replace(ch, "" if ch != " " else " ")
            changes.append(f"removed {n} invisible character(s) U+{ord(ch):04X}")
    for src, dst in LEX["typography"].items():
        n = text.count(src)
        if n:
            if src == "\u2014":
                text = re.sub(r"\s*\u2014\s*", " - ", text)
            else:
                text = text.replace(src, dst)
            changes.append(f"replaced {n} x U+{ord(src):04X} with '{dst.strip() or dst}'")
    n = len(re.findall(r",\s+and\b", text))
    if n:
        text = re.sub(r",(\s+)and\b", r"\1and", text)
        changes.append(f"removed {n} comma(s) before 'and'")
    for phrase, rep in sorted(LEX["phrases"].items(), key=lambda kv: -len(kv[0])):
        pat = re.compile(r"\b" + re.escape(phrase) + r"\b", re.I)
        hits = pat.findall(text)
        if hits:
            text = pat.sub(rep, text)
            changes.append(f"'{phrase}' -> '{rep}'" if rep else f"DELETED '{phrase}' - rewrite that sentence by hand")
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r" +([,.!?])", r"\1", text)
    text = re.sub(r"^[ ,]+", "", text, flags=re.M)
    return text, changes


def score(text):
    """Five checks, 20 points each. Returns (total, findings)."""
    findings, total = [], 0
    low = text.lower()
    slop = [p for p in LEX["phrases"] if re.search(r"\b" + re.escape(p) + r"\b", low)]
    s = max(0, 20 - 5 * len(slop)); total += s
    findings.append(("VOCABULARY", s, f"{len(slop)} stock phrase(s): {', '.join(slop[:6])}" if slop else "clean"))

    marks = sum(text.count(c) for c in LEX["invisible"]) + text.count("\u2014") + len(re.findall(r",\s+and\b", text))
    s = max(0, 20 - 4 * marks); total += s
    findings.append(("TYPOGRAPHY", s, f"{marks} em dash / invisible char / comma-before-and" if marks else "clean"))

    struct = [label for pat, label in LEX["structural"] if re.search(pat, text, re.I | re.M)]
    s = max(0, 20 - 7 * len(struct)); total += s
    findings.append(("STRUCTURE", s, "; ".join(struct) if struct else "clean"))

    sents = [x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x]
    lens = [len(x.split()) for x in sents] or [0]
    mean = sum(lens) / len(lens)
    var = sum((l - mean) ** 2 for l in lens) / len(lens)
    s = 20 if len(lens) < 3 or var >= 12 else int(20 * var / 12); total += s
    findings.append(("RHYTHM", s, f"sentence length spread {var:.0f} (flat rhythm reads machine-made)" if s < 20 else "varied"))

    concrete = len(re.findall(r"\d|\b(am|pm|km|kg|rs|inr|usd|min|mins|hours?|days?|monday|tuesday|wednesday|thursday|friday|saturday|sunday|street|road|nagar)\b", low))
    s = min(20, concrete * 5); total += s
    findings.append(("SPECIFICITY", s, f"{concrete} concrete detail(s): numbers, times, places, units"))
    return total, findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="draft file, or - for stdin")
    ap.add_argument("--fix", action="store_true", help="rewrite the draft")
    ap.add_argument("--report", action="store_true", help="list every change")
    ap.add_argument("--out", help="write the cleaned text here instead of in place")
    a = ap.parse_args()
    src = sys.stdin.read() if a.file == "-" else Path(a.file).read_text(encoding="utf-8")
    before, _ = score(src)
    text, changes = clean(src) if a.fix else (src, [])
    after, findings = score(text)
    print("HUMANIZER  " + ("before %d  after %d" % (before, after) if a.fix else "score %d" % after) + " / 100")
    for name, s, note in findings:
        print(f"  {name:<12}{s:>3}/20  {note}")
    if a.report and changes:
        print("CHANGES")
        for c in changes:
            print("  - " + c)
    if a.fix:
        if a.out or a.file != "-":
            Path(a.out or a.file).write_text(text, encoding="utf-8")
        else:
            print("\n" + text)
    deleted = [c for c in changes if c.startswith("DELETED")]
    weak = [name for name, s, _ in findings if s == 0]
    if deleted:
        verdict = f"{len(deleted)} phrase(s) were deleted, so those sentences need a human rewrite before shipping"
    elif weak:
        verdict = f"add {', '.join(weak).lower()} before shipping"
    else:
        verdict = "ship it" if after >= 80 else "rewrite the flagged parts" if after >= 60 else "reads machine-made, rewrite"
    print(f"VERDICT  {verdict}")
    if deleted:
        print("REWRITE THESE ORIGINAL SENTENCES BY HAND (do not ship the mechanical cut):")
        phrases = [c.split("'")[1] for c in deleted]
        for sent in re.split(r"(?<=[.!?])\s+", src.strip()):
            if any(ph in sent.lower().replace("\u2019", "'") for ph in phrases):
                print("  > " + sent.strip())


if __name__ == "__main__":
    main()
