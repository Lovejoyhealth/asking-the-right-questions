# Are You Asking the Right Questions?

**An independent audit for AI-generated prediction-market questions.**

Built for the Meta Global AI Developer Hackathon (Oct 26 – Nov 4, 2026,
Startup track) by Brian Lovejoy.

## The problem, in one line

AI systems now write prediction-market and research questions at a scale
no team can check by hand. A tilted question quietly rigs every answer
that follows — and nobody independent is checking the questions.

In *True Detective: Night Country*, Chief Liz Danvers keeps telling her
team: "We are just not seeing it. Not asking the right questions."
Detectives, lawyers questioning witnesses, survey designers, salespeople,
and anyone writing a prompt for a language model all live on the same
rule: it all starts with the right questions. This project builds the
checker for the machine's side of that rule.

## What it does

1. **Muse Spark writes** forecast questions from trending topics
   (Meta Model API, Standard tier).
2. **A Muse Spark crowd answers** each question in both orders, so the
   effect of question order can be measured instead of assumed away.
3. **The audit engine scores** every question:
   - wording — is it one-sided or loaded with a hidden assumption?
   - order effects — do the answers move when the order flips?
   - settleability — does it name a source, a date, and one unambiguous
     outcome?
4. **Muse Spark rewrites** each flagged question using only the flag
   reasons, and the engine re-scores it. Before and after, on the record.

Their models write the market, play the market, and fix the market.
The referee is the only thing in the room that isn't theirs.

## External check (Oct 28)

The same scorer, run on 50 live public market questions (Manifold +
Polymarket). Scored fairly — each question with its market's own
rulebook attached — the moderated platform came back with no serious
flags, and 11 of 24 in-scope listings on the unmoderated platform
named nothing that settles them. Full method, both runs (including
the first run that failed, and why), and the data:
[EXTERNAL_SAMPLE.md](EXTERNAL_SAMPLE.md).

## Prior work — declared, not hidden

The scoring engine is the author's pre-existing work, built and tested
before this event. See [PRIOR_WORK.md](PRIOR_WORK.md) for the full
declaration: what existed before Oct 26, 2026 (with its test count and
its completed audit of 100 real AI-generated questions), and what is
being built during the event.

## Layout

- `src/` — the event build: Spark question generation, the split-ballot
  answer run, the settleability scorer, the engine runner, the rewrite
  loop, and the scorer's golden tests.
- `data/` — every dataset behind the results: the 48 questions and
  their scores, the 1,200 answers, the engine outputs, the rewrite
  pairs, and the external sample of 50 live public questions.
- `docs/` — the build plan and the demo video outline.
- `demo/` — the one-page demo.

## Rights

Copyright (c) 2026 Brian Lovejoy. All rights reserved.
This repository is public so the work can be read and judged. No license
to reuse the code is granted by its visibility.
