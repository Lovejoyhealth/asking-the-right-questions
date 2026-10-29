# External sample — run 1 (text-only), Wed Oct 28, 2026

Approved by Brian Oct 28 evening (Lever 1 of the Impact memo: score the
world's questions, not just ours). Run by Atlas the same evening, $0.
Data: `data/external-sample.json` (harness:
the sampling rule below is complete).

## Sampling rule (fixed before fetching)

Manifold + Polymarket public APIs, no account or key. Only markets
still open; only yes/no questions; volume order, first 25 per platform
passing a fixed politics/war keyword screen. Scored with the repo
scorer, unmodified except TODAY set to the run date (2026-10-28).

## Raw result — NOT a usable headline

50 questions; **47 flagged with something; all 25 Polymarket questions
flagged.** Flag totals: NO_DATE 35, NO_SOURCE_CUE 37,
NUMERIC_CLAIM_REVIEW 5, PAST_DATE 1. A hand spot-check showed the count
is an artifact of the instrument, not a fact about the questions:

- The scorer does not read ISO dates (`2026-11-01`), ordinal dates
  (`October 30th`), or year-less dates (`October 28`) — most NO_DATE
  flags are false alarms on questions that carry a date.
- Platform questions keep their settling source in the market's rules
  page, not the question text — most NO_SOURCE_CUE flags are the same
  story.
- The single PAST_DATE (Polymarket gold, "Week of October 26 2026") is
  a misread: the phrase names the week STARTING Oct 26; the market was
  open until Oct 30.
- The keyword screen leaked two political questions (X16 White House
  Press Secretary; X17 El-Sayed vs. Talarico, Senate candidates). Both
  are marked here and excluded from any claim.

## What was learned

The scorer is calibrated for standalone questions (survey items,
AI-generated questions) that must carry their deadline and source
inside the text. Platform markets carry both in metadata and rules, so
a text-only check is the wrong shape of test for them. "47 of 50" must
never be quoted as a finding.

## Run 2 — the fair rescore (approved by Brian, run Oct 28 evening)

Same 50 questions, no resampling, scored with each market's listed
close date (in prose) and its own published resolution-rules text
attached — the moderator view. 48 of 50 listings had rules text.
full scored texts saved in
`data/external-sample-rescore.json`. Scorer unmodified except
TODAY = run date.

Raw movement: any-flag fell from 47 of 50 to 35 of 50, but run 2's
REVIEW-level flags (DOUBLE_BARRELED 24, NUMERIC_CLAIM_REVIEW 29,
LOADED_CUE 5) are mostly triggered by the rules prose itself, so they
are NOT counted as question flaws. The finding tier is FLAG level,
hand-checked one by one:

- **Polymarket: 0 genuine FLAG-level flaws in 25.** Text-only had
  flagged all 25; with their own rules attached, every listing names
  its settling source. The checker does not cry wolf on a moderated
  platform.
- **Manifold: 7 in-scope listings (of 23) name no settling source
  anywhere in the listing** — question plus rules combined
  (X02, X05, X06, X07, X10, X12, X13). X06 has no rules text at all.
  Several are personal or spam listings that are not settleable
  questions at all (a celebrity-gossip item, an SEO headline).
- **Four Manifold flags cleared on the full-rules hand-check** (the
  scorer's word list has no cue for what these listings name): X01
  names BaseScan as its "Source of Truth" with a verification URL;
  X04 and X15 state explicitly that the creator resolves on stated
  criteria; X14 resolves on the named LessWrong 2026 Annual Review
  vote. Flagged by the word list, cleared by a reader. (Correction,
  Oct 28: an earlier version of this page said 11 of 24. That count
  read the flags without reading each listing's full rules text, and
  its denominator was wrong — both politics leaks were Manifold, so
  in-scope Manifold is 23. The corrected count above was verified by
  two independent full-rules reads.)
- **Both run-2 PAST_DATE flags are artifacts, excluded:** X49 is the
  run-1 "week of October 26" misread again; X19's "May 2025" is a data
  baseline inside the rules text, not a deadline.
- The X16 politics leak also survives as NO_SOURCE_CUE; it stays
  excluded from all claims, like X17.

## The honest headline (only these numbers may be quoted)

"We ran the audit on 50 live public market questions. Read fairly —
with each market's own rulebook attached — the moderated platform
(Polymarket, 25 questions) came back with no serious flags, and 7 of
23 in-scope listings on the unmoderated platform (Manifold) named
nothing that settles them."

## Status

Run 1 = logged null (wrong-shaped test). Run 2 = the fair test, with a
modest, hand-verified finding (count corrected Oct 28, see above).
