#!/usr/bin/env python3
"""Check a finished .excalidraw board for the failures the owner has rejected.

Usage: python3 audit_board.py board.excalidraw

Prints a list of problems and a short summary. Exit code 1 if any problem
was found, so you cannot report "done" while it still fails.
Each check matches a correction in SKILL.md section 2.
"""
import json, re, sys, collections

PLACEHOLDER = re.compile(r"place image|todo|tbd|lorem|insert (figure|image)|\bxxx\b", re.I)
MAX_LINE = 78          # characters per line in a note; longer lines run off the frame
MAX_BOX_W = 760        # px; a free note wider than this is an unwrapped paragraph
MIN_FONT = 14          # body text smaller than this is unreadable at normal zoom


def main(path):
    d = json.load(open(path))
    els = [e for e in d["elements"] if not e.get("isDeleted")]
    problems = []

    # unique ids
    ids = [e["id"] for e in els]
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dup:
        problems.append(f"{len(dup)} duplicate ids, e.g. {dup[:3]} (boxes will render empty)")

    texts = [e for e in els if e["type"] == "text"]
    free = [e for e in texts if not e.get("containerId")]
    bound = [e for e in texts if e.get("containerId")]

    # placeholders
    for e in texts:
        if PLACEHOLDER.search(e.get("text", "")):
            problems.append(f"placeholder text: {e['text'][:60]!r}")

    # long unwrapped lines and wide boxes
    long_lines = [e for e in free if max((len(l) for l in e["text"].split("\n")), default=0) > MAX_LINE
                  and e.get("fontSize", 16) <= 17]
    if long_lines:
        problems.append(f"{len(long_lines)} notes have a line longer than {MAX_LINE} characters "
                        f"(hard-wrap with newlines); first: {long_lines[0]['text'][:50]!r}")
    wide = [e for e in free if e.get("width", 0) > MAX_BOX_W and e.get("fontSize", 16) <= 17]
    if wide:
        problems.append(f"{len(wide)} notes are wider than {MAX_BOX_W}px (one long paragraph per box)")

    small = [e for e in texts if e.get("fontSize", 16) < MIN_FONT
             and not re.fullmatch(r"[\d.\-+%\s]*", e.get("text", ""))]   # axis tick numbers are exempt
    if small:
        problems.append(f"{len(small)} text elements use a font below {MIN_FONT}")

    # paragraphs that are one block of prose with no numbers, no list, no example
    prose = []
    for e in free:
        t = e["text"]
        if len(t) > 350 and "\n" not in t.strip():
            prose.append(e)
    if prose:
        problems.append(f"{len(prose)} notes are a single 350+ character paragraph with no line breaks")

    # bare one-word map nodes
    bare = [e for e in bound if len(e["text"].split()) <= 2 and e.get("fontSize", 16) <= 18]
    if bound and len(bare) / len(bound) > 0.35:
        problems.append(f"{len(bare)} of {len(bound)} boxed labels are one or two words "
                        f"(map leaves must read 'term - meaning')")

    # overlapping free notes (grid bucket)
    cell = 400
    grid = collections.defaultdict(list)
    for i, e in enumerate(free):
        for gx in range(int(e["x"] // cell), int((e["x"] + e["width"]) // cell) + 1):
            for gy in range(int(e["y"] // cell), int((e["y"] + e["height"]) // cell) + 1):
                grid[(gx, gy)].append(i)
    seen, overlaps = set(), []
    for lst in grid.values():
        for a in range(len(lst)):
            for b in range(a + 1, len(lst)):
                i, j = lst[a], lst[b]
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                A, B = free[i], free[j]
                w = min(A["x"] + A["width"], B["x"] + B["width"]) - max(A["x"], B["x"])
                h = min(A["y"] + A["height"], B["y"] + B["height"]) - max(A["y"], B["y"])
                if w > 6 and h > 6 and w * h > 0.15 * min(A["width"] * A["height"], B["width"] * B["height"]):
                    overlaps.append((A["text"][:25], B["text"][:25]))
    if overlaps:
        problems.append(f"{len(overlaps)} pairs of notes overlap, e.g. {overlaps[0]}")

    # variety: a board that is all text is the failure in reference/style-gallery/B3
    kinds = collections.Counter(e["type"] for e in els)
    nontext = kinds["image"] + kinds["arrow"] + kinds["line"] + kinds["diamond"] + kinds["ellipse"]
    if kinds["image"] == 0:
        problems.append("no images at all: formulas must be rendered images and figures must be embedded")
    if len(texts) > 40 and nontext < 0.3 * len(texts):
        problems.append(f"mostly text ({len(texts)} text vs {nontext} drawn/image elements): "
                        f"add anatomy, tables, flows, figures")

    # worked numbers: at least some notes should hold digits with an operator
    worked = [e for e in free if re.search(r"\d+\s*[x×*/+\-=]\s*\d+", e["text"])]
    if len(free) > 20 and len(worked) < 0.1 * len(free):
        problems.append(f"only {len(worked)} notes show a worked calculation; add numbers to the mechanism notes")

    # questions without answers
    q = [e for e in free if re.search(r"^\s*Q\d*[.:)]", e["text"], re.M)]
    a = [e for e in free if re.search(r"^\s*A\d*[.:)]|\bAnswer\b", e["text"], re.M)]
    if q and len(a) < len(q) * 0.5:
        problems.append(f"{len(q)} question notes but only {len(a)} with an answer; every question needs an exam-ready answer")

    print(f"elements {len(els)}  text {len(texts)}  images {kinds['image']}  arrows {kinds['arrow']}  "
          f"worked-number notes {len(worked)}")
    if problems:
        print("\nPROBLEMS")
        for p in problems:
            print(" -", p)
        sys.exit(1)
    print("no problems found by these checks (this does not replace looking at the render)")


if __name__ == "__main__":
    main(sys.argv[1])
