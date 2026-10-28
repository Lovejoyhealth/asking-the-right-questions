# src

Event-built code for "Are You Asking the Right Questions?" (built during
the event, Oct 26–27, 2026). The audit engine core itself is pre-existing
work — see ../PRIOR_WORK.md.

- `audit_questions.py` — the deterministic checklist scorer. Standard
  library only, no API calls. Run it from anywhere:
  `python3 src/audit_questions.py` reads `data/questions.json` and
  writes `data/question_scores.json` + `data/question_scores.md`.
  Re-running it reproduces the committed scores exactly.
- `generate_answers.py` — the split-ballot answer run (one plain Muse
  Spark forecaster, order shuffled every run). Importing it runs
  nothing. Running it needs a Meta Model API helper (set
  `SPARK_CHAT_PATH`) and a Standard-tier API key, and it costs money —
  about $3.04 at the Oct 27 run's prices. Its output is the committed
  `data/answers.json`.
- `run_audit.py` — the first-pass engine runner (permutation nulls,
  model-free order statistics, the position-effect shuffle test). Needs
  numpy plus the prior-work engine source, which is not in this repo:
  set `SURVEY_ENGINE_SRC` to the folder holding the engine's `nulls.py`
  and `noncommutative.py`. Its docstring tells the full two-pass story,
  including the Oct 27 second pass that ran the Pyro Bayesian track.
- `test_audit_questions.py` — golden tests for the scorer:
  `python3 -m unittest discover -s src` re-scores the frozen questions
  and checks every count and flag against the committed scores.
