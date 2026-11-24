#!/usr/bin/env python3
"""Lint an Instagram caption the way the feed shows it.

    python3 caption_check.py caption.txt [--keywords "sourdough,bakery"] [--city Pune]
"""
import argparse, re
from pathlib import Path

ASKS = r"\b(comment|dm|message|whatsapp|call|visit|apply|register|book|fill|tap|link in bio|save|share)\b"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--keywords", default="")
    ap.add_argument("--city", default="", help="city or area that should appear in the caption")
    a = ap.parse_args()
    text = Path(a.file).read_text(encoding="utf-8").strip()
    fold = text[:125].replace("\n", " / ")
    print("WHAT THE FEED SHOWS BEFORE '... more'")
    print("+" + "-" * 66 + "+")
    for i in range(0, len(fold), 64):
        print("| " + fold[i:i + 64].ljust(64) + " |")
    print("+" + "-" * 66 + "+")
    issues = []
    first = text.split("\n", 1)[0]
    if len(first) > 125:
        issues.append("Line one is cut mid-thought by the fold. End it at a cliff before 125 characters.")
    tags = re.findall(r"#\w+", text)
    if len(tags) > 5:
        issues.append(f"{len(tags)} hashtags. Use 3 to 5 specific ones.")
    if not tags:
        issues.append("No hashtags. Add 3 to 5 local and specific ones.")
    asks = set(m.lower() for m in re.findall(ASKS, text, re.I))
    if not asks:
        issues.append("No ask. Add one action.")
    elif len(asks) > 2:
        issues.append(f"Several asks ({', '.join(sorted(asks))}). Keep one.")
    if a.city and a.city.lower() not in text.lower():
        issues.append(f"City '{a.city}' missing. Instagram search reads captions, add the location in plain words.")
    if "\u2014" in text:
        issues.append("Em dash found. Use a hyphen.")
    if re.search(r",\s+and\b", text):
        issues.append("Comma before 'and' found. Remove it (house style).")
    for kw in [k.strip() for k in a.keywords.split(",") if k.strip()]:
        if kw.lower() not in text.lower():
            issues.append(f"Keyword missing: '{kw}'")
    print(f"{len(text)} characters, {len(text.split())} words, {len(tags)} hashtags")
    for i in issues:
        print("  - " + i)
    print("CLEAN" if not issues else f"{len(issues)} issue(s)")


if __name__ == "__main__":
    main()
