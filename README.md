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

## Prior work — declared, not hidden

The scoring engine is the author's pre-existing work, built and tested
before this event. See [PRIOR_WORK.md](PRIOR_WORK.md) for the full
declaration: what existed before Oct 26, 2026 (with its test count and
its completed audit of 100 real AI-generated questions), and what is
being built during the event.

## Layout

- `src/` — the event build: Spark generation, the answering crowd, the
  settleability score, the rewrite loop (lands day by day, Oct 27 – 31).
- `docs/` — the build plan and the demo video outline.
- `demo/` — the one-page demo (lands Oct 31 – Nov 1).

## Rights

Copyright (c) 2026 Brian Lovejoy. All rights reserved.
This repository is public so the work can be read and judged. No license
to reuse the code is granted by its visibility.
