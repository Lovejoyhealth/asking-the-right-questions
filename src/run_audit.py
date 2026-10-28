#!/usr/bin/env python3
"""Smallest faithful engine runner for the hackathon answer run (step 2).

Reads files/answer-run-2026-10-27.json (300 Spark forecaster calls: 12 topics
x 25 shuffled runs) and writes files/engine-run-2026-10-27.json.

WHAT RAN (prior-work code, loaded directly from
~/workspace/survey-bias-audit-extract/src/survey_bias_audit/ because the
package __init__ needs reportlab, which is not installed):
- nulls.permutation_null: column-shuffle permutation null for every pairwise
  correlation between questions in a topic (destroys between-item coupling,
  keeps each question's marginal distribution).
- noncommutative.qq_residual and .order_effect: the projective-model order
  statistics on dichotomized joint tables (probability >= 50 counts as YES;
  stated plainly wherever used). order_effect is the total-variation distance
  between the two question orders, on aligned labels.
- noncommutative.null_order_effect: the 95th-percentile order-effect reading
  expected when the true effect is zero, at the pair's arm size.

WHAT DID NOT RUN, and why:
- The Pyro Bayesian track (bayes.py, LKJ + NUTS) did NOT run: torch and
  pyro-ppl are not installed in this sandbox. In its place, each position
  effect carries a plain normal-approximation 95% interval, LABELED as an
  approximation, never as the Pyro fit.
- The PennyLane noncommutative module did NOT run as a fitted model: no
  pennylane, no torch. The qq_residual / order_effect statistics above are
  the same module's model-free statistics, not a fitted quantum model.
- No human respondents: the "respondents" here are 25 repeated calls to ONE
  Muse Spark forecaster per topic. Results describe Spark's answering
  behaviour, not human forecasters. That limit is stated in every output.

Position effect (the headline order measurement): for each question, the mean
probability when the question was asked FIRST minus the mean when it was asked
later. Null: the same difference after shuffling which runs count as "first"
(2000 permutations, fixed seed). Two-sided p.
Verdict rule (fixed before looking at results, stated here): an order effect
is FLAGGED only if p < 0.05 AND |effect| >= 10 points. p < 0.05 with a smaller
effect is SUGGESTIVE. Everything else is NO EFFECT FOUND. With 48 questions
tested at 0.05, about 2-3 false flags are expected by chance alone; the
report says so rather than hiding it.
"""

CORRECTION (Oct 27, 2026): the "WHAT DID NOT RUN" section below is the
first pass's original claim and it was wrong — torch, pyro and pennylane
were installed all along in the survey engine's own venv; this runner
executed under the system Python. A second pass the same day ran the Pyro
Bayesian track, the fitted noncommutative model, and the PennyLane circuit
verification for real (hidden_files/run_engine_full.py and
run_pair_fits.py; outputs files/engine-run-full-2026-10-27.json and
files/engine-run-pair-fits-2026-10-27.json). All reports were patched.

import importlib.util
import itertools
import json
import sys

import numpy as np

GOAL = "/home/hatch/workspace/goals/meta-global-ai-developer-hackathon-entry"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


BASE = "/home/hatch/workspace/survey-bias-audit-extract/src/survey_bias_audit/"
nulls = load("engine_nulls", BASE + "nulls.py")
nc = load("engine_nc", BASE + "noncommutative.py")

with open(f"{GOAL}/files/answer-run-2026-10-27.json") as f:
    run = json.load(f)
with open(f"{GOAL}/files/working-set-2026-10-26.json") as f:
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
    for a, b in itertools.permutations(qids, 2):
        pass
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
with open(f"{GOAL}/files/engine-run-2026-10-27.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"questions=48 flagged={len(flagged)} suggestive={len(suggestive)} "
      f"mean_abs_effect={results['summary']['mean_absolute_position_effect_points']} "
      f"max_abs={results['summary']['max_absolute_position_effect_points']} "
      f"pairs={len(results['pairs'])} pairs_clearing_bar={len(pairs_clearing)}")
for r in flagged + suggestive:
    print(f"  {r['verdict']} {r['question_id']} effect={r['position_effect_first_minus_later']} p={r['permutation_p']}")
