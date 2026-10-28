# RESULTS — what this run found

Repo: https://github.com/Lovejoyhealth/asking-the-right-questions (public showcase repo;
the engine core itself stays private and is declared in PRIOR_WORK.md).

## What was measured, in plain words

Muse Spark — one plain forecaster, no personalities — answered the repo's 48
frozen questions (12 topics x 4) 25 times per topic, with the question order
shuffled every run: 300 calls, 1,200 probabilities, about $3.04 of event credit.
Then the audit measured whether a question's probability changed just because of
where it sat in the list (the **position effect**: average when asked first,
minus average when asked later), whether pairs of questions moved together
(**coupling**), and whether question pairs behaved differently in the two orders
(**QQ order check**). Every effect is reported next to its own shuffle test:
the same statistic recomputed on shuffled data, so a reading can be judged
against what pure chance produces.

## Headline

**No broad order effect in Spark's answers on this set.** Mean absolute position effect 2.91 points; 43 of 48 questions: no effect found; 1 flagged; 4 suggestive. No question pair cleared the chance bar on the QQ order check (0 of 72). The repo's headline number is therefore a small one, honestly stated: order moved Spark's answers by about 2.91 points on average, with one question (Q32) as the single lead worth re-testing.

## Per-question verdicts

Flag rule, fixed before the run: FLAGGED needs shuffle p < 0.05 AND |effect| >= 10 points;
p < 0.05 with a smaller effect is SUGGESTIVE; otherwise NO EFFECT FOUND.
With 48 tests at 0.05, about 2-3 false alarms are expected from chance alone.

| Question | Topic | Mean | First | Later | Effect | Shuffle p | Verdict |
|---|---|---|---|---|---|---|---|
| Q01 | AI models and releases | 98.92 | 99.25 | 98.86 | 0.39 | 0.9925 | NO EFFECT FOUND |
| Q02 | AI models and releases | 51.36 | 51.43 | 51.33 | 0.1 | 1.0 | NO EFFECT FOUND |
| Q03 | AI models and releases | 74.84 | 77.57 | 73.78 | 3.79 | 0.1954 | NO EFFECT FOUND |
| Q04 | AI models and releases | 98.84 | 99.29 | 98.67 | 0.62 | 0.7206 | NO EFFECT FOUND |
| Q05 | US politics and the 2026 midterms | 66.04 | 65.0 | 66.24 | -1.24 | 0.3493 | NO EFFECT FOUND |
| Q06 | US politics and the 2026 midterms | 78.84 | 81.22 | 77.5 | 3.72 | 0.1384 | NO EFFECT FOUND |
| Q07 | US politics and the 2026 midterms | 26.08 | 26.0 | 26.11 | -0.11 | 1.0 | NO EFFECT FOUND |
| Q08 | US politics and the 2026 midterms | 6.56 | 8.17 | 6.05 | 2.11 | 0.0185 | SUGGESTIVE |
| Q09 | the US economy and jobs | 19.84 | 14.33 | 22.94 | -8.6 | 0.0055 | SUGGESTIVE |
| Q10 | the US economy and jobs | 64.28 | 67.86 | 62.89 | 4.97 | 0.6442 | NO EFFECT FOUND |
| Q11 | the US economy and jobs | 27.0 | 20.0 | 28.33 | -8.33 | 0.4298 | NO EFFECT FOUND |
| Q12 | the US economy and jobs | 71.16 | 78.0 | 69.45 | 8.55 | 0.1134 | NO EFFECT FOUND |
| Q13 | interest rates and the Federal Reserve | 83.44 | 85.2 | 83.0 | 2.2 | 0.6737 | NO EFFECT FOUND |
| Q14 | interest rates and the Federal Reserve | 67.88 | 61.75 | 70.76 | -9.01 | 0.1834 | NO EFFECT FOUND |
| Q15 | interest rates and the Federal Reserve | 82.84 | 83.5 | 82.71 | 0.79 | 0.7941 | NO EFFECT FOUND |
| Q16 | interest rates and the Federal Reserve | 8.4 | 7.62 | 8.76 | -1.14 | 0.4713 | NO EFFECT FOUND |
| Q17 | housing and rent | 1.64 | 1.45 | 1.79 | -0.33 | 0.1754 | NO EFFECT FOUND |
| Q18 | housing and rent | 68.28 | 75.0 | 66.6 | 8.4 | 0.2069 | NO EFFECT FOUND |
| Q19 | housing and rent | 36.12 | 32.0 | 37.15 | -5.15 | 0.0825 | NO EFFECT FOUND |
| Q20 | housing and rent | 0.24 | 0.5 | 0.19 | 0.31 | 0.2274 | NO EFFECT FOUND |
| Q21 | climate and extreme weather | 20.84 | 19.17 | 21.37 | -2.2 | 0.2704 | NO EFFECT FOUND |
| Q22 | climate and extreme weather | 17.0 | 14.4 | 17.65 | -3.25 | 0.1949 | NO EFFECT FOUND |
| Q23 | climate and extreme weather | 93.16 | 94.5 | 92.74 | 1.76 | 0.1949 | NO EFFECT FOUND |
| Q24 | climate and extreme weather | 59.12 | 61.5 | 58.0 | 3.5 | 0.1259 | NO EFFECT FOUND |
| Q25 | public health | 32.2 | 28.4 | 33.15 | -4.75 | 0.2899 | NO EFFECT FOUND |
| Q26 | public health | 0.24 | 0.14 | 0.28 | -0.13 | 0.6342 | NO EFFECT FOUND |
| Q27 | public health | 2.44 | 2.0 | 2.58 | -0.58 | 0.2349 | NO EFFECT FOUND |
| Q28 | public health | 64.56 | 64.71 | 64.5 | 0.21 | 0.988 | NO EFFECT FOUND |
| Q29 | space and science | 60.64 | 60.5 | 60.68 | -0.18 | 0.9975 | NO EFFECT FOUND |
| Q30 | space and science | 45.2 | 39.75 | 47.76 | -8.01 | 0.015 | SUGGESTIVE |
| Q31 | space and science | 7.0 | 4.75 | 7.43 | -2.68 | 0.043 | SUGGESTIVE |
| Q32 | space and science | 72.0 | 63.29 | 75.39 | -12.1 | 0.0045 | FLAGGED |
| Q33 | pro sports championships | 12.0 | 11.83 | 12.05 | -0.22 | 0.952 | NO EFFECT FOUND |
| Q34 | pro sports championships | 10.16 | 10.5 | 10.1 | 0.4 | 0.5362 | NO EFFECT FOUND |
| Q35 | pro sports championships | 5.72 | 5.0 | 6.0 | -1.0 | 0.3858 | NO EFFECT FOUND |
| Q36 | pro sports championships | 15.68 | 16.12 | 15.47 | 0.65 | 0.5257 | NO EFFECT FOUND |
| Q37 | movies and entertainment | 30.92 | 32.58 | 29.38 | 3.2 | 0.3463 | NO EFFECT FOUND |
| Q38 | movies and entertainment | 4.36 | 5.0 | 4.11 | 0.89 | 0.1984 | NO EFFECT FOUND |
| Q39 | movies and entertainment | 17.64 | 16.75 | 17.81 | -1.06 | 0.7736 | NO EFFECT FOUND |
| Q40 | movies and entertainment | 6.72 | 7.0 | 6.7 | 0.3 | 0.8771 | NO EFFECT FOUND |
| Q41 | energy and gas prices | 10.0 | 8.2 | 10.45 | -2.25 | 0.1354 | NO EFFECT FOUND |
| Q42 | energy and gas prices | 14.28 | 13.71 | 14.5 | -0.79 | 0.6767 | NO EFFECT FOUND |
| Q43 | energy and gas prices | 7.28 | 6.43 | 7.61 | -1.18 | 0.3278 | NO EFFECT FOUND |
| Q44 | energy and gas prices | 34.84 | 34.67 | 34.89 | -0.23 | 0.9675 | NO EFFECT FOUND |
| Q45 | big tech companies | 65.68 | 71.14 | 63.56 | 7.59 | 0.2449 | NO EFFECT FOUND |
| Q46 | big tech companies | 94.04 | 96.43 | 93.11 | 3.32 | 0.1 | NO EFFECT FOUND |
| Q47 | big tech companies | 6.84 | 4.8 | 7.35 | -2.55 | 0.086 | NO EFFECT FOUND |
| Q48 | big tech companies | 15.96 | 12.33 | 17.11 | -4.77 | 0.052 | NO EFFECT FOUND |

## The flagged question

**Q32** — Will NASA confirm discovery of a new potentially habitable exoplanet by September 30, 2027? — effect -12.1 points (first 63.29 over 7 runs vs later 75.39), shuffle p = 0.0045. Plain reading: asked first, Spark scored it about 12 points lower. This is a lead for a re-test with more runs, not a proven flaw: only 7 runs had it first.

## Coupling (answers moving together)

Pairs with |correlation| >= 0.5, each against its column-shuffle null (1,000 shuffles):

- Q01 / Q04 (AI models and releases): r = 0.847, null mean -0.006, p = 0.002.
- Q09 / Q10 (the US economy and jobs): r = 0.674, null mean -0.002, p = 0.001.
- Q09 / Q11 (the US economy and jobs): r = 0.81, null mean 0.0, p = 0.001.
- Q09 / Q12 (the US economy and jobs): r = 0.532, null mean 0.004, p = 0.004.
- Q10 / Q11 (the US economy and jobs): r = 0.724, null mean -0.004, p = 0.001.
- Q10 / Q12 (the US economy and jobs): r = 0.69, null mean -0.003, p = 0.001.
- Q11 / Q12 (the US economy and jobs): r = 0.505, null mean 0.002, p = 0.002.
- Q47 / Q48 (big tech companies): r = 0.59, null mean -0.003, p = 0.003.

Coupling is not an order effect: it says the forecaster's answers to the two questions tracked each other inside the same call. It is part of what the questions did to the answers, so it is reported, not hidden.

## Pair order checks (QQ): 0 of 72 cleared the chance bar

Joint YES/NO tables were built by splitting probabilities at 50 (stated plainly: 49 and 51 are nearly the same belief but land on opposite sides of the split). Largest readings:

- Q09 / Q10 (the US economy and jobs): order reading 0.338, QQ residual 0.338, chance bar 0.455 — below the bar.
- Q10 / Q11 (the US economy and jobs): order reading 0.263, QQ residual -0.192, chance bar 0.417 — below the bar.
- Q14 / Q16 (interest rates and the Federal Reserve): order reading 0.25, QQ residual 0.25, chance bar 0.417 — below the bar.
- Q29 / Q31 (space and science): order reading 0.235, QQ residual 0.235, chance bar 0.5 — below the bar.
- Q45 / Q46 (big tech companies): order reading 0.222, QQ residual 0.222, chance bar 0.556 — below the bar.

## What is prior work and what is new here

PRIOR WORK (declared in PRIOR_WORK.md, never presented as event work):
- The BQNN audit engine core: the Bayesian (Pyro) model, the PennyLane order
  module, and the null-check machinery — built before this event, with 145 tests.
- The Oct 20 Octagon 100-question wording audit (separate data, separate run).

EVENT-BUILT (this event only):
- The 48-question generation set (Spark, Oct 26).
- The checklist scorer and its scores on those 48 questions.
- This answer-generation run (Spark, 300 calls) and the integration runner that
  fed the answers to the measurement (this repo's src/run_audit.py).
- The rewrite loop and its before/after pairs.
- The demo page.

## Exactly what machinery ran — and what did not

RAN (prior-work code, loaded directly from the engine source):
- `nulls.permutation_null` — column-shuffle nulls for the correlations.
- `noncommutative.qq_residual`, `.order_effect`, `.null_order_effect` — the
  model-free order statistics and the chance bar.
- This runner's own first-vs-later shuffle test (2,000 permutations per question).

SECOND PASS (Oct 27) — the full engine ran, in the engine's own Python
environment (the first pass used the wrong Python; the packages were never
missing from the machine):
- The Pyro Bayesian track (LKJ prior + NUTS, 0 divergences): posterior
  coupling for all 72 pairs — 12 have 95% ranges excluding zero, and 9 of the
  10 pairs the classical shuffle test flagged at p < 0.01 are corroborated in
  direction with ranges excluding zero. Per-question position-effect ranges
  in the second-pass report (data/engine-run-full-2026-10-27.json) are Pyro
  fits from this pass, not approximations; the per-question records in
  data/engine_results.json still carry the first pass's
  normal-approximation intervals, labeled as such.
- The fitted noncommutative (quantum-style) model ran two ways and is NOT
  evidence here: fitted jointly it fit badly, and fitted per pair it implied
  order effects about 2.5x the directly measured ones. Reported, not hidden —
  see the full engine report. The verdicts rest on the direct measurement
  plus the Bayesian corroboration.
- PennyLane ran as independent verification: the qubit-circuit implementation
  of the order statistics agreed with the main implementation to machine
  precision (within 6.7e-16) on all 12 topic cross-checks.
Raw second-pass outputs: data/engine-run-full-2026-10-27.json and
data/engine-run-pair-fits-2026-10-27.json.

## Limits (same as the full report)

One AI forecaster, not humans. First-position samples are small (2-12 runs per
question). Pair tables split probabilities at 50. 48 tests invite chance hits.
Wording/settleability flags are a separate layer (see the checklist scores):
a question can be clean here and badly worded, or vice versa.
