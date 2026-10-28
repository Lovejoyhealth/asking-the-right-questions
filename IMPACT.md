# IMPACT — what this repo proves, in public, reproducibly

This is the repo-scoped impact case. It is narrower than the general
impact case on purpose: it claims only what a judge who opens this repo
can see, run, and check for themselves. The general case — the size of
the market for question-checking, the Octagon background audit, the
roadmap from audit to LLM auditing to training — lives in the
submission draft. This file is about what *this repo* proves.

## The problem, in one paragraph (plain words)

AI systems now write prediction-market and survey questions at a scale
no team can check by hand. A **prediction-market question** is a
question with a date and a yes/no outcome that people bet on ("Will X
happen by date Y?"). If the question is broken — its deadline already
passed, no source named to decide the answer, a number nobody verified
— then every answer, price, and decision after it is built on sand.
Survey tools already check *wording*. Nobody in this repo's pipeline
checks what the questions *do to the answers* — except this audit.

## What this repo proves (each claim is checkable in this repo)

### 1. Triage is reproducible: 48 questions, 31 flagged

Run `src/audit_questions.py` on the frozen question set in
`data/questions.json` and you get the same scores in
`data/question_scores.json`:

- **31 of 48 questions flagged.** 5 with a deadline already in the
  past (PAST_DATE), 9 naming no settling source (NO_SOURCE_CUE),
  21 resting on a specific number a human must verify
  (NUMERIC_CLAIM_REVIEW). Counts add past 31 because some questions
  carry two flags.
- **Wording honestly clean on the loaded-language check:** no
  loaded-cue flag fired on any of the 48. The triage failures are
  settleability failures, not word-bias failures — and that
  distinction is itself a finding a wording-only checker would miss
  in the other direction.
- What this proves: a fixed, written rule checker — no AI judgment,
  no hidden weights — can catch un-settleable questions in a
  machine-written set, question by question, with the evidence quoted
  next to each flag.

### 2. The rewrite loop works on form — and says where it stops

`data/rewrite_pairs.json` holds 14 before/after pairs. Spark rewrote
only the questions flagged for a past date or a missing source, fixing
only the flagged problem:

- **13 of 14 cleared the flag they were rewritten for.** The exception
  is Q05, which still names no settling source after its rewrite.
- Precisely: 9 of 14 have no flags at all after rewriting; 4 more keep
  only the number-check note (their date/source flag cleared, the
  number still needs a human); Q05 still carries its missing-source
  flag.
- Featured pair (Q14, the Fed rate-cut question): "Will the Federal
  Reserve announce at least one interest rate cut before June 30,
  2026?" (past date) → "Will the Federal Reserve announce at least
  one interest rate cut before June 30, 2027, according to the
  Federal Reserve?" (clean).
- **Every new date is marked "needs human date check."** The scorer
  checks that a date is present and in the future; it does not verify
  the date is the correct real-world date. The loop fixes the *form*
  of the question. Verifying dates and numbers is still a human's job,
  and this repo says so on the face of the pairs.

### 3. The measurement runs on public data — and its headline is a small, honest number

`src/run_audit.py` feeds the frozen answer data in `data/answers.json`
(300 Spark calls, 1,200 probabilities: one plain Spark forecaster, no
personalities, each topic's 4 questions answered 25 times with the
order shuffled every run) to the measurement, producing
`data/engine_results.json` and `RESULTS.md`. **The repo's headline
number is whatever this run found — and it is small:**

- **Mean absolute position effect: 2.91 points.** ("Position effect"
  = average probability when a question was asked first, minus its
  average when asked later.)
- **No broad order effect: 43 of 48 questions no effect found, 1
  flagged, 4 suggestive.** The flagged question is Q32 (space and
  science): −12.1 points when asked first (63.29 over 7 runs vs 75.39
  later), shuffle-test p = 0.0045 — a lead to re-test, not a proven
  flaw, because with 48 tests about 2–3 false alarms are expected from
  chance alone.
- **0 of 72 question pairs cleared the chance bar** on the pair-order
  (QQ) check.
- **Coupling reported, not hidden:** 8 pairs moved together far more
  than shuffled data does (correlations 0.51–0.85), including the
  jobs-topic questions moving together. Coupling is not an order
  effect; it is part of what the questions did to the answers.

Why a small headline is still impact: the repo's claim is not "we
found a huge effect." The claim is "here is an instrument that
measures, on public data, with its own shuffle comparisons, whether
order moved the answers — and on this set it mostly did not, with one
lead worth re-testing." A checker that only ever shouts is not a
checker. A checker that reports a near-null honestly, with its
comparisons attached, is the thing a platform can trust before money
rides on the questions.

### 4. The event-built vs prior-work line is drawn in the repo itself

See `PRIOR_WORK.md` and `RESULTS.md`:

- **Prior work (declared, never presented as event work):** the BQNN
  audit engine core (Bayesian/Pyro model + PennyLane order module +
  shuffled-data null checks, 145 tests), and the Oct 20, 2026 Octagon
  100-question wording audit (separate data, separate run).
- **Event-built (this event only):** the 48-question generation set,
  the checklist scorer, this answer-generation run, the integration
  runner (`src/run_audit.py`), the rewrite loop, and the demo page.
- **Exactly what machinery ran:** the engine's permutation shuffle
  test for correlations and its model-free order statistics (QQ
  residual, order reading, chance bar), plus this runner's own
  first-vs-later shuffle test (2,000 shuffles per question).
- **Second pass (Oct 27):** the Pyro Bayesian track ran (in the
  engine's own environment — the first pass used the wrong Python):
  coupling posteriors for all 72 pairs and Pyro position-effect ranges
  replacing the first pass's approximations. The fitted
  quantum-style model also ran and is not load-bearing: it overstates
  order effects on this data, so the repo's claims rest on the direct
  measurement plus the Bayesian corroboration. PennyLane ran as
  circuit verification (12 of 12 cross-checks at machine precision).

## What this repo does NOT prove (stated, not buried)

- **Not human forecasters.** The "respondents" are 25 repeated calls
  to one AI model. Nothing here describes how humans would answer.
- **Not real markets.** These are Spark-written questions answered by
  Spark. No real money, no real market prices, no settled outcomes.
- **Not a customer or a pilot.** No paying customer, no pilot, no
  adoption is claimed by this repo. Customer discovery is separate
  work, and its answers — not this repo's hopes — decide what comes
  next.
- **Not verified dates or numbers.** Rewrite dates need a human date
  check; numbers flagged NUMERIC_CLAIM_REVIEW need a human source
  check. The repo fixes form; humans verify facts.
- **The fitted model is not the measurement.** The fitted
  quantum-style model ran (see above) and overstates order effects
  on this data. The measurement this repo stands behind is the
  direct order comparison against shuffled nulls, corroborated by
  the Pyro Bayesian track.
- **Not the general market case.** The size of the market for
  question-checking, and the Octagon background audit, are argued in
  the submission draft with their own sources. This repo proves the
  instrument runs and reports honestly on public data; the market
  argument is not proven by this repo alone, and this file does not
  pretend otherwise.

## What comes next, in repo terms (not promises)

1. **Re-test Q32** with more first-position runs — the single flagged
   lead, currently resting on 7 first-position runs.
2. **Human date and number checks** on all 14 rewrites and all 21
   number-check flags, recorded as a new data file when done.
3. **Fold the second pass's fitted Bayesian ranges into the summary
  data file** — the Bayesian-track run itself is DONE (Oct 27 second
  pass; outputs in `data/engine-run-full-2026-10-27.json`). What
  remains is carrying its fitted per-question ranges into
  `data/engine_results.json`, whose per-question records still hold
  the first pass's labeled normal-approximation intervals.
4. **A pilot question set from a real platform or survey buyer** —
   the same pipeline, on questions that are not ours — which is the
   step that turns a demonstrated instrument into a demonstrated
   service.

## The one-line version

This repo proves, on frozen public data anyone can re-run, that a
machine-written question set can be triaged for settleability (31 of
48 flagged), repaired in form (13 of 14 rewrites clearing their flag),
and measured for what its questions did to its answers (average order
move 2.91 points; no broad effect; one lead to re-test) — with every
limit, and the fitted model that ran and failed, stated on the
face of the results.
