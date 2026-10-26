# Prior-work disclosure — DRAFT for Brian's review (2026-10-26)

Purpose: the kickoff states the submission must declare what code existed
before the event. This is that declaration, written plainly. Nothing here is
inflated: every item below existed and was tested before Oct 26, 2026, and
the commit history in Brian's GitHub account (Lovejoyhealth) is the
timestamped record. Brian edits and approves before any of it is submitted.

---

## What existed before the hackathon (pre-existing code, Brian's own work)

1. **The audit engine** (repo: Lovejoyhealth/survey-bias-audit, private;
   extraction workspace: survey-bias-audit-extract). Built across 2025–2026
   as a survey-question bias audit tool:
   - A **Bayesian model (Pyro)** that scores questions and answers and
     reports its answer as a range (a best guess with an uncertainty band),
     never a single overconfident number.
   - A **quantum order-effects module (PennyLane)** that measures whether
     the ORDER questions are asked in changes the answers — the effect
     classical probability says should not happen.
   - **Shuffled-data null checks** (permutation testing): the same analysis
     re-run on scrambled data, so an effect is only claimed when it beats
     its own scrambled baseline.
   - Classical statistics track (item coupling, question-order bias,
     item-total checks) run alongside the Bayesian track; a finding prints
     only when tracks agree and survive the null checks.
   - **145 automated tests**, passing, as of the Oct 22, 2026 application.

2. **A completed audit of real AI-generated questions** (Oct 20, 2026):
   100 questions from 20 Octagon AI research reports scored for one-sided
   wording and hidden assumptions. Result: about 1 in 8 questions
   one-sided; an independent second scoring agreed on 95 of 100. This run
   used the pre-existing engine as-is and is part of the evidence the
   application was judged on.

3. **Supporting workflow code**: report harvesting, hand-labeling of
   evidence into scored cards, and one-page PDF generation
   (proven Oct 20–25, 2026 on the survey and Octagon work above).

## What is being built DURING the event (Oct 26 – Nov 4, 2026)

1. Muse Spark question generation via the Meta Model API (Spark as writer).
2. A Spark forecaster crowd that answers each question in both orders
   (Spark as the answering crowd).
3. The settleability score — new this week: does the question name a
   source, a date, and one unambiguous outcome?
4. The rewrite loop: Spark rewrites a flagged question using only the
   flag reasons; the pre-existing engine re-scores it (Spark as fixer;
   the engine — pre-existing — stays the referee).
5. The one-page demo and this submission's video.

## The honest one-liner for the submission form

"The scoring engine is my pre-existing work, declared above with its
history. Everything that touches Muse Spark — generation, the answering
crowd, the settleability score, the rewrite loop, and the demo — was built
during the event. Their models write the market, play the market, and
fix the market. The referee is mine, and it was already built."
