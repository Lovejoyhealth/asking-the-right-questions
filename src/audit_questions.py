#!/usr/bin/env python3
"""Deterministic question scorer for "Are You Asking the Right Questions?"

Scores forecast/survey questions on the TEXT of the question alone.
No AI, no API calls, no randomness: the same question always gets the
same flags. Standard library only.

Two families of checks:

SETTLEABILITY -- can this question ever be settled cleanly?
  NO_DATE                 no date / deadline phrase found in the wording
  PAST_DATE               the deadline in the wording is already past
  NO_SOURCE_CUE           no explicit settling-authority cue in the wording
                          (means "no cue in the text", NOT "unsettleable")
  DOUBLE_BARRELED_REVIEW  looks like two events in one question (REVIEW:
                          a human checks; this is never a verdict)

WORDING -- does the question push one answer?
  LOADED_CUE              a presupposition / loaded phrase from the
                          project's Octagon rubric list (REVIEW level)
  NUMERIC_CLAIM_REVIEW    a number + unit claim a human must verify
                          against a source (REVIEW level; the code never
                          asserts a figure is wrong)

Every flag carries the exact evidence text it matched.

Usage:
    python3 audit_questions.py [questions.json] [scores.json] [scores.md]
Defaults point at the frozen 2026-10-26 working set and outputs.
"""

import json
import re
import sys
from datetime import date

# The day the working set was frozen and scored. Deadlines before this
# date cannot be settled in the future anymore.
TODAY = date(2026, 10, 26)

DEFAULT_INPUT = (
    "/home/hatch/workspace/goals/meta-global-ai-developer-hackathon-entry/"
    "files/working-set-2026-10-26.json"
)
DEFAULT_JSON_OUT = (
    "/home/hatch/workspace/goals/meta-global-ai-developer-hackathon-entry/"
    "files/question-scores-2026-10-26.json"
)
DEFAULT_MD_OUT = (
    "/home/hatch/workspace/goals/meta-global-ai-developer-hackathon-entry/"
    "files/question-scores-2026-10-26.md"
)

# ---------------------------------------------------------------- dates

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5,
    "june": 6, "july": 7, "august": 8, "september": 9, "october": 10,
    "november": 11, "december": 12,
}
MONTH_ALT = "|".join(MONTHS)

# "December 31, 2026" or "January 31 2027" (comma optional)
FULL_DATE_RE = re.compile(
    r"\b(" + MONTH_ALT + r")\s+(\d{1,2}),?\s+(\d{4})\b", re.IGNORECASE
)
# "December 2026" (month + year, no day)
MONTH_YEAR_RE = re.compile(
    r"\b(" + MONTH_ALT + r")\s+(\d{4})\b", re.IGNORECASE
)
# bare year reference, e.g. "in 2026"
BARE_YEAR_RE = re.compile(r"\b(?:in|during|year|season)\s+(?:the\s+)?(\d{4})\b",
                           re.IGNORECASE)

# Words that mark a date as the settling deadline.
DEADLINE_CUES = ("by", "before", "on", "through", "as of", "as reported by",
                 "as certified by", "until", "deadline")


def find_dates(text):
    """Return list of (parsed_date, matched_text, char_position)."""
    found = []
    spans = []
    for m in FULL_DATE_RE.finditer(text):
        month = MONTHS[m.group(1).lower()]
        try:
            d = date(int(m.group(3)), month, int(m.group(2)))
        except ValueError:
            continue
        found.append((d, m.group(0), m.start()))
        spans.append(m.span())
    for m in MONTH_YEAR_RE.finditer(text):
        if any(s <= m.start() < e for s, e in spans):
            continue  # already part of a full date
        month = MONTHS[m.group(1).lower()]
        # A month-year reference resolves to the END of that month for
        # deadline purposes (the outcome is known by then at the latest).
        if month == 12:
            d = date(int(m.group(2)), 12, 31)
        else:
            d = date(int(m.group(2)), month + 1, 1).toordinal()
            d = date.fromordinal(d - 1)
        found.append((d, m.group(0), m.start()))
        spans.append(m.span())
    if not found:
        for m in BARE_YEAR_RE.finditer(text):
            # A bare year reference resolves to the end of that year.
            found.append((date(int(m.group(1)), 12, 31), m.group(0), m.start()))
    return sorted(found, key=lambda t: t[2])


def pick_deadline(text, dates):
    """The deadline is the last date that follows a deadline cue word;
    if no date carries a cue, fall back to the latest date found."""
    best = None
    for d, matched, pos in dates:
        window = text[max(0, pos - 20):pos].lower()
        if any(window.rstrip().endswith(cue) or (cue + " ") in window
               for cue in DEADLINE_CUES):
            if best is None or pos > best[2]:
                best = (d, matched, pos)
    if best is not None:
        return best
    return max(dates, key=lambda t: t[0])


# ------------------------------------------------------- source cues

# Explicit settling-authority cues. If NONE of these appear in the
# wording, the question carries no visible statement of who or what
# settles it. This flag is about the text only.
SOURCE_CUES = [
    "according to", "as reported by", "as certified by", "reported by",
    "official", "announce", "announcement", "declare", "certify",
    "certified", "confirm", "report", "reports",
    "federal reserve", "bureau of labor statistics", "census bureau",
    "noaa", "nasa", "cdc", "who", "fda",
    "championship", "world series", "super bowl", "win", "wins",
    "academy awards",
]

# ------------------------------------------------------- loaded cues

# Presupposition / loaded phrases, from the project's Octagon audit
# rubric. REVIEW level: a human decides whether the phrase actually
# loads this particular question.
LOADED_CUES = [
    "admit", "fail to", "fails to", "failed to",
    "refuse to", "refuses to", "refused to",
    "still", "despite", "even though", "so-called",
]

# ------------------------------------------------------- numeric claims

UNIT_WORDS = [
    "million", "billion", "trillion", "percent", "%", "points",
    "dollars", "cents", "acres", "millimeters", "units",
]
NUMERIC_CLAIM_RE = re.compile(
    r"\$?\d[\d,]*(?:\.\d+)?\s*(?:" + "|".join(map(re.escape, UNIT_WORDS)) + r")"
    r"(?:\s+\w+){0,2}",
    re.IGNORECASE,
)
DOLLAR_AMOUNT_RE = re.compile(r"\$\d[\d,]*(?:\.\d+)?")

# ------------------------------------------------------- double-barreled

EITHER_OR_RE = re.compile(r"\beither\b.+\bor\b", re.IGNORECASE)
# Small verb list used only to test whether BOTH sides of an " and "
# look like their own clause. Heuristic, REVIEW level by design.
CLAUSE_VERBS = [
    "be", "is", "are", "was", "were", "will", "win", "wins", "hold",
    "holds", "release", "releases", "report", "reports", "announce",
    "announces", "exceed", "exceeds", "reach", "reaches", "launch",
    "launches", "approve", "approves", "elect", "elects", "confirm",
    "confirms", "declare", "declares", "remain", "remains", "close",
    "closes", "settle", "settles", "gross", "certify", "certifies",
]


def check_double_barreled(text):
    """Return evidence string if the question looks double-barreled."""
    m = EITHER_OR_RE.search(text)
    if m:
        return m.group(0)
    if " and " in text.lower():
        left, _, right = text.lower().partition(" and ")
        left_has_verb = any(
            re.search(r"\b" + v + r"\b", left) for v in CLAUSE_VERBS)
        right_has_verb = any(
            re.search(r"\b" + v + r"\b", right) for v in CLAUSE_VERBS)
        if left_has_verb and right_has_verb:
            return " and ".join(
                [left.strip()[-60:], right.strip()[:60]])
    return None


# ------------------------------------------------------- scoring

FLAG_REASONS = {
    "NO_DATE": "No date or deadline in the wording, so there is no "
               "moment when the answer becomes final.",
    "PAST_DATE": "The deadline in the wording is already in the past "
                 "(before Oct 26, 2026), so the question can no longer "
                 "be settled in the future.",
    "NO_SOURCE_CUE": "The wording names no source or authority that "
                     "settles the answer (no 'according to', official "
                     "body, announcement, or result cue in the text).",
    "DOUBLE_BARRELED_REVIEW": "The question may ask about two events at "
                              "once; if they split, no single yes/no "
                              "answer is clean. A human should check.",
    "LOADED_CUE": "The wording contains a phrase that presupposes or "
                  "loads one side of the answer. A human should check "
                  "whether it actually pushes this question.",
    "NUMERIC_CLAIM_REVIEW": "The question states a specific number. A "
                            "human must verify that figure against a "
                            "source before the question is used; the "
                            "scorer does not judge the figure itself.",
}


def score_question(q):
    text = q["question"]
    lower = text.lower()
    flags = []

    # 1. Deadline
    dates = find_dates(text)
    if not dates:
        flags.append({
            "code": "NO_DATE", "level": "FLAG",
            "evidence": "no date phrase found in the question text",
        })
    else:
        d, matched, _ = pick_deadline(text, dates)
        if d < TODAY:
            flags.append({
                "code": "PAST_DATE", "level": "FLAG",
                "evidence": matched + " (parsed as " + d.isoformat() + ")",
            })

    # 2. Source cue
    hit = next((c for c in SOURCE_CUES if c in lower), None)
    if hit is None:
        flags.append({
            "code": "NO_SOURCE_CUE", "level": "FLAG",
            "evidence": "no settling-authority cue from the scorer's "
                        "cue list appears in the question text",
        })

    # 3. Double-barreled (REVIEW)
    ev = check_double_barreled(text)
    if ev:
        flags.append({
            "code": "DOUBLE_BARRELED_REVIEW", "level": "REVIEW",
            "evidence": ev,
        })

    # 4. Loaded cues (REVIEW)
    for cue in LOADED_CUES:
        m = re.search(r"\b" + re.escape(cue) + r"\b", lower)
        if m:
            flags.append({
                "code": "LOADED_CUE", "level": "REVIEW",
                "evidence": text[m.start():m.end()],
            })

    # 5. Numeric claims (REVIEW)
    seen = set()
    for m in NUMERIC_CLAIM_RE.finditer(text):
        claim = m.group(0).strip()
        if claim.lower() not in seen:
            seen.add(claim.lower())
            flags.append({
                "code": "NUMERIC_CLAIM_REVIEW", "level": "REVIEW",
                "evidence": claim,
            })
    for m in DOLLAR_AMOUNT_RE.finditer(text):
        claim = m.group(0).strip()
        if claim.lower() not in seen:
            seen.add(claim.lower())
            flags.append({
                "code": "NUMERIC_CLAIM_REVIEW", "level": "REVIEW",
                "evidence": claim,
            })

    return {
        "id": q["id"], "topic": q["topic"], "question": text,
        "flags": flags,
    }


def main():
    in_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    json_out = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_JSON_OUT
    md_out = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MD_OUT

    with open(in_path, encoding="utf-8") as f:
        questions = json.load(f)

    results = [score_question(q) for q in questions]

    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # ---- summary markdown
    counts = {}
    for r in results:
        for fl in r["flags"]:
            counts[fl["code"]] = counts.get(fl["code"], 0) + 1
    flagged = [r for r in results if r["flags"]]

    lines = []
    lines.append("# Question scores — working set of Oct 26, 2026")
    lines.append("")
    lines.append(
        "Deterministic text scoring by `src/audit_questions.py` "
        "(standard library only, no AI calls). Scored against the "
        "freeze date Oct 26, 2026. FLAG = a plain finding from the "
        "wording itself. REVIEW = a human should look; the scorer is "
        "not issuing a verdict.")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append(f"- Questions scored: {len(results)}")
    lines.append(f"- Questions with at least one flag: {len(flagged)}")
    for code in sorted(counts):
        lines.append(f"- {code}: {counts[code]}")
    lines.append("")
    lines.append("## Flagged questions, with reasons")
    for r in flagged:
        lines.append("")
        lines.append(f"### {r['id']} — {r['topic']}")
        lines.append(f"> {r['question']}")
        for fl in r["flags"]:
            lines.append(
                f"- **{fl['code']}** ({fl['level']}): "
                f"{FLAG_REASONS[fl['code']]} "
                f"Evidence: \"{fl['evidence']}\"")
    lines.append("")

    with open(md_out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(json.dumps({"scored": len(results), "counts": counts}, indent=2))


if __name__ == "__main__":
    main()
