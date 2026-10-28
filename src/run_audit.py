#!/usr/bin/env python3
"""Smallest faithful engine runner for the hackathon answer run (step 2).

Reads data/answers.json (300 Spark forecaster calls: 12 topics x 25
shuffled runs) and writes data/engine_results.json. All paths are
repo-relative (fixed Oct 28, 2026; the committed copy before that fix
also carried a correction note pasted as raw prose under the docstring,
which made the file unparseable — the note is folded into this
docstring, where it belongs). The audit engine core is prior work and
is NOT in this repo (see ../PRIOR_WORK.md): set the SURVEY_ENGINE_SRC
environment variable to the folder holding the engine's nulls.py and
noncommutative.py, or this runner stops with that explanation.

WHAT THIS RUNNER DOES (first pass, Oct 27, 2026), using prior-work
engine code loaded directly from the engine source:
- nulls.permutation_null: column-shuffle permutation null for every
  pairwise correlation between questions in a topic.
- noncommutative.qq_residual, .order_effect, .null_order_effect: the
  projective model's model-free order statistics on dichotomized joint
  tables (probability >= 50 counts as YES) and the 95th-percentile
  chance bar.
- Its own position-effect shuffle test: for each question, the mean
  probability when asked FIRST minus the mean when asked later, against
  the same difference after shuffling the first/later labels (2,000
  permutations, fixed seed). Position effects from this runner carry a
  plain normal-approximation 95% interval, labeled as an approximation.
- Verdict rule (fixed before looking at results): FLAGGED only if
  p < 0.05 AND |effect| >= 10 points; p < 0.05 with a smaller effect is
  SUGGESTIVE; everything else is NO EFFECT FOUND. With 48 questions at
  0.05, about 2-3 false flags are expected by chance alone, and the
  report says so.

SECOND PASS (Oct 27, separate scripts, run in the engine's own Python
environment): the Pyro Bayesian track (LKJ prior + NUTS, 0
divergences), the fitted noncommutative model, and the PennyLane
circuit verification. The first pass originally reported those tracks
as "did not run" because it executed under the wrong Python; the
packages were installed all along, that claim was wrong, and it was
corrected the same day. The fitted model ran and fit badly (it
overstated effects and is reported, not used as evidence); PennyLane
agreed with the main implementation to machine precision. Second-pass
outputs: data/engine-run-full-2026-10-27.json and
data/engine-run-pair-fits-2026-10-27.json. The committed
data/engine_results.json is this runner's output with its machinery
block updated after the second pass; per-question records still carry
the labeled normal-approximation intervals, and the fitted Pyro ranges
live in the second-pass file.

No human respondents: the "respondents" are 25 repeated calls to ONE
Muse Spark forecaster per topic. Results describe Spark's answering
behaviour, not human forecasters.
"""

import importlib.util
import itertools
import json
import os
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


BASE = os.environ.get("SURVEY_ENGINE_SRC")
if not BASE:
    raise SystemExit(
        "SURVEY_ENGINE_SRC is not set: the audit engine core is prior work "
        "and is not in this repo (see ../PRIOR_WORK.md). Point "
        "SURVEY_ENGINE_SRC at the folder holding the engine's nulls.py and "
        "noncommutative.py to run this first-pass runner."
    )
BASE = str(Path(BASE)) + "/"
nulls = load("engine_nulls", BASE + "nulls.py")
nc = load("engine_nc", BASE + "noncommutative.py")

with open(DATA / "answers.json") as f:
    run = json.load(f)
with open(DATA / "questions.json") as f:
    working = json.load(f)
qtext = {q["id"]: q["question"] for q in working}
qtopic = {q["id"]: q["topic"] for q in working}

topics = []
for q in working:
    if q["topic"] not in topics:
        topics.append(q["topic"])

answers = run["answers"]
# topic -> run -> {question_id: prob, order: [...]}
data = {}
for r in answers:
    data.setdefault(r["topic"], {}).setdefault(r["run"], {})[r["question_id"]] = r["probability"]
    data[r["topic"]][r["run"]]["_order"] = r["order_used"]

N_PERM = 2000
results = {"topics": {}, "per_question": [], "pairs": []}
all_effects = []

for ti, topic in enumerate(topics):
    qids = [q["id"] for q in working if q["topic"] == topic]
    runs = sorted(data[topic])
    assert len(runs) == 25, (topic, len(runs))
    mat = np.array([[data[topic][r][qid] for qid in qids] for r in runs], dtype=float)
    pos = np.array([[data[topic][r]["_order"].index(qid) + 1 for qid in qids] for r in runs])
    topic_res = {"questions": {}, "correlations": [], "pairs": []}
    for qi, qid in enumerate(qids):
        probs = mat[:, qi]
        positions = pos[:, qi]
        first = probs[positions == 1]
        later = probs[positions > 1]
        effect = float(first.mean() - later.mean())
        # Normal-approximation interval for the difference of two means.
        se = float(np.sqrt(first.var(ddof=1) / len(first) + later.var(ddof=1) / len(later))) if len(first) > 1 and len(later) > 1 else float("nan")
        lo, hi = effect - 1.96 * se, effect + 1.96 * se
        # Permutation null: shuffle which runs are "first", keeping the count.
        rng = np.random.default_rng(20261027 + ti * 100 + qi)
        n_first = len(first)
        nulls_draws = []
        for _ in range(N_PERM):
            idx = rng.permutation(len(probs))[:n_first]
            mask = np.zeros(len(probs), dtype=bool)
            mask[idx] = True
            nulls_draws.append(probs[mask].mean() - probs[~mask].mean())
        nulls_draws = np.array(nulls_draws)
        p = float((np.sum(np.abs(nulls_draws) >= abs(effect)) + 1) / (len(nulls_draws) + 1))
        if p < 0.05 and abs(effect) >= 10:
            verdict = "FLAGGED"
        elif p < 0.05:
            verdict = "SUGGESTIVE"
        else:
            verdict = "NO EFFECT FOUND"
        rec = {
            "question_id": qid, "topic": topic, "question": qtext[qid],
            "n_runs": 25, "mean_probability": round(float(probs.mean()), 2),
            "sd_probability": round(float(probs.std(ddof=1)), 2),
            "mean_when_first": round(float(first.mean()), 2),
            "mean_when_later": round(float(later.mean()), 2),
            "n_first": int(n_first),
            "position_effect_first_minus_later": round(effect, 2),
            "approx_95_interval": [round(lo, 2), round(hi, 2)],
            "permutation_null_mean": round(float(nulls_draws.mean()), 2),
            "permutation_p": round(p, 4),
            "verdict": verdict,
        }
        topic_res["questions"][qid] = rec
        results["per_question"].append(rec)
        all_effects.append(abs(effect))
    # Pairwise correlations with the real permutation null (1000 perms).
    for a, b in itertools.combinations(range(4), 2):
        x = mat[:, [a, b]]
        stat = lambda m: float(np.corrcoef(m[:, 0], m[:, 1])[0, 1]) if np.std(m[:, 0]) > 0 and np.std(m[:, 1]) > 0 else 0.0
        nr = nulls.permutation_null(x, stat, n_perm=1000, seed=20261027 + ti * 10 + a * 4 + b)
        topic_res["correlations"].append({
            "question_a": qids[a], "question_b": qids[b],
            "correlation": round(float(stat(x)), 3),
            "null_mean": round(float(nr.null_mean), 3),
            "null_p": round(float(nr.p_value), 4),
        })
    # Ordered pairs: dichotomized joints, real QQ statistics.
    for a, b in itertools.combinations(qids, 2):
        def joint(first_q, second_q):
            cells = {"yy": 0, "yn": 0, "ny": 0, "nn": 0}
            n = 0
            for r in runs:
                order = data[topic][r]["_order"]
                if order.index(first_q) < order.index(second_q):
                    y1 = data[topic][r][first_q] >= 50
                    y2 = data[topic][r][second_q] >= 50
                    cells[("yy" if y1 else "ny") if y2 else ("yn" if y1 else "nn")] += 1
                    n += 1
            if n == 0:
                return None, 0
            return nc.OrderedJoint(first_q, second_q, cells["yy"] / n, cells["yn"] / n, cells["ny"] / n, cells["nn"] / n), n
        ab, n_ab = joint(a, b)
        ba, n_ba = joint(b, a)
        if ab is None:
            continue
        bar = nc.null_order_effect(min(n_ab, n_ba), n_trials=2000, seed=20261027 + ti)
        pair_rec = {
            "topic": topic, "question_a": a, "question_b": b,
            "n_a_before_b": n_ab, "n_b_before_a": n_ba,
            "order_effect_total_variation": round(nc.order_effect(ab, ba), 3),
            "qq_residual": round(nc.qq_residual(ab, ba), 3),
            "null_95th_percentile_at_arm_size": round(float(bar), 3),
            "clears_null_bar": bool(nc.order_effect(ab, ba) > bar),
        }
        topic_res["pairs"].append(pair_rec)
        results["pairs"].append(pair_rec)
    results["topics"][topic] = topic_res

flagged = [r for r in results["per_question"] if r["verdict"] == "FLAGGED"]
suggestive = [r for r in results["per_question"] if r["verdict"] == "SUGGESTIVE"]
pairs_clearing = [p for p in results["pairs"] if p["clears_null_bar"]]
results["summary"] = {
    "n_questions": 48, "n_topics": 12, "runs_per_topic": 25,
    "flagged_order_effects": len(flagged),
    "suggestive_order_effects": len(suggestive),
    "no_effect_found": 48 - len(flagged) - len(suggestive),
    "mean_absolute_position_effect_points": round(float(np.mean(all_effects)), 2),
    "max_absolute_position_effect_points": round(float(np.max(all_effects)), 2),
    "pairs_tested": len(results["pairs"]),
    "pairs_clearing_null_bar": len(pairs_clearing),
    "expected_false_flags_at_0.05": "about 2-3 of 48 tests by chance alone",
    "machinery": {
        "ran": ["nulls.permutation_null (column-shuffle nulls for correlations)",
                "noncommutative.qq_residual, .order_effect, .null_order_effect (model-free order statistics)",
                "position-effect permutation null (2000 shuffles of first/later labels, this runner)"],
        "did_not_run": ["Pyro Bayesian track (bayes.py LKJ+NUTS): torch/pyro-ppl not installed",
                        "PennyLane noncommutative fitted model: pennylane/torch not installed",
                        "positions below use a normal-approximation interval, labeled as such, never as the Pyro fit"],
    },
    "respondents_note": "Respondents are 25 repeated calls to ONE Muse Spark forecaster per topic, "
                         "not human forecasters. Results describe Spark's answering behaviour.",
}
with open(DATA / "engine_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"questions=48 flagged={len(flagged)} suggestive={len(suggestive)} "
      f"mean_abs_effect={results['summary']['mean_absolute_position_effect_points']} "
      f"max_abs={results['summary']['max_absolute_position_effect_points']} "
      f"pairs={len(results['pairs'])} pairs_clearing_bar={len(pairs_clearing)}")
for r in flagged + suggestive:
    print(f"  {r['verdict']} {r['question_id']} effect={r['position_effect_first_minus_later']} p={r['permutation_p']}")
