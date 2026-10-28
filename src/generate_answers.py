#!/usr/bin/env python3
"""Split-ballot answer generation for the hackathon working set (step 2).

ONE plain Muse Spark forecaster, no personas. For each of 12 topics, the
topic's 4 questions are presented 25 times with the question order shuffled
every run (seeded, so order_used is reproducible). Each call asks for a YES
probability 0-100 per question. Results append incrementally to a JSONL file
so a partial run is never lost; a final JSON assembly is written at the end.

Cost note (Standard tier, per connector doc): $1.25/M input, $4.25/M output.
Pilot call Oct 26: 188 prompt + 2568 completion tokens (~$0.011/call).
300 calls estimate ~$3.40, inside the $20 cumulative cap.
"""
import json
import os
import random
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Paths are repo-relative (fixed Oct 28, 2026). Importing this module
# runs nothing: the run lives in main() at the bottom.
REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
WORKING = DATA / "questions.json"
OUT_JSONL = DATA / "answer-run-progress.jsonl"
OUT_JSON = DATA / "answers.json"
USAGE_LOG = DATA / "answer-run-usage.json"
# The Meta Model API helper script lives outside this repo; point
# SPARK_CHAT_PATH at it. Running main() also needs a Standard-tier API
# key in the helper's environment, and it costs money (about $3.04 for
# the full 300-call run at the Oct 27 run's prices).
SPARK = os.environ.get("SPARK_CHAT_PATH", "")

SYSTEM = "You are a forecaster. Reply only with the requested numbered probabilities, no explanation."
LINE_RE = re.compile(r"(Q\d{2})\s*:\s*(\d{1,3})")

# NOTE (Oct 28, 2026): everything below used to execute on import.
# It now lives in main(); importing this module has no side effects.
def main():
    if not SPARK or not Path(SPARK).is_file():
        raise SystemExit(
            "SPARK_CHAT_PATH is not set to the Meta Model API helper "
            "script. Running this regenerates data/answers.json with "
            "300 Muse Spark calls and costs money (about $3.04 at "
            "the Oct 27 run's prices). See src/README.md."
        )
    with open(WORKING) as f:
        questions = json.load(f)

    topics = []
    seen = set()
    for q in questions:
        if q["topic"] not in seen:
            seen.add(q["topic"])
            topics.append(q["topic"])
    by_topic = {t: [q for q in questions if q["topic"] == t] for t in topics}
    assert len(topics) == 12 and all(len(by_topic[t]) == 4 for t in topics)

    # Resume: skip (topic, run) pairs already recorded.
    done = set()
    try:
        with open(OUT_JSONL) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["topic"], r["run"]))
                except json.JSONDecodeError:
                    pass
    except FileNotFoundError:
        pass

    usage = {"prompt_tokens": 0, "completion_tokens": 0, "calls": 0, "failed": 0}
    try:
        with open(USAGE_LOG) as f:
            usage = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    lock = threading.Lock()


    def one_call(topic, run, order):
        qs = {q["id"]: q["question"] for q in by_topic[topic]}
        lines = "\n".join(f"{i+1}. {qid}: {qs[qid]}" for i, qid in enumerate(order))
        prompt = (
            "For each question below, give your probability that the answer is YES, "
            "as a number from 0 to 100. Reply with exactly 4 lines, one per question, "
            "in the order shown, like this: Q13: 42. No other text.\n" + lines
        )
        proc = subprocess.run(
            [sys.executable, SPARK, prompt, "--model", "muse-spark-1.3",
             "--max-tokens", "4000", "--system", SYSTEM],
            capture_output=True, text=True, timeout=120,
        )
        payload = json.loads(proc.stdout)
        if not payload.get("ok"):
            raise RuntimeError(f"spark call failed: {payload}")
        probs = {}
        for m in LINE_RE.finditer(payload["reply"]):
            qid, val = m.group(1), int(m.group(2))
            if qid in qs and 0 <= val <= 100:
                probs[qid] = val
        if set(probs) != set(order):
            raise ValueError(f"unparsed reply for {topic} run {run}: {payload['reply']!r}")
        with lock:
            usage["prompt_tokens"] += payload["usage"].get("prompt_tokens", 0)
            usage["completion_tokens"] += payload["usage"].get("completion_tokens", 0)
            usage["calls"] += 1
            with open(USAGE_LOG, "w") as f:
                json.dump(usage, f, indent=2)
        return probs


    def do_run(task):
        topic, run = task
        rng = random.Random(20261027 + topics.index(topic) * 100 + run)
        order = [q["id"] for q in by_topic[topic]]
        rng.shuffle(order)
        last_err = None
        for attempt in range(3):
            try:
                probs = one_call(topic, run, order)
                break
            except Exception as e:  # retry same order; a retry is a fresh forecaster sample
                last_err = e
        else:
            with lock:
                usage["failed"] += 1
            print(f"FAILED {topic} run {run}: {last_err}", flush=True)
            return
        rows = [{"topic": topic, "run": run, "order_used": order,
                 "question_id": qid, "probability": probs[qid]} for qid in order]
        with lock:
            with open(OUT_JSONL, "a") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")
        print(f"done {topic} run {run} probs={probs}", flush=True)


    tasks = [(t, run) for t in topics for run in range(1, 26) if (t, run) not in done]
    print(f"topics={len(topics)} tasks_total={len(topics)*25} remaining={len(tasks)} already_done={len(done)}", flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(do_run, tasks))

    rows = []
    with open(OUT_JSONL) as f:
        for line in f:
            rows.append(json.loads(line))
    rows.sort(key=lambda r: (topics.index(r["topic"]), r["run"], r["order_used"].index(r["question_id"])))
    cost = usage["prompt_tokens"] / 1e6 * 1.25 + usage["completion_tokens"] / 1e6 * 4.25
    out = {
        "generated": "2026-10-27",
        "model": "muse-spark-1.3",
        "method": "ONE plain Muse Spark forecaster, no personas. Each topic's 4 questions presented "
                  "25 times with question order shuffled every run (split-ballot). "
                  "Nothing planted: the forecaster's own probabilities, as returned.",
        "n_topics": 12, "runs_per_topic": 25, "n_rows": len(rows),
        "usage": usage, "estimated_cost_usd": round(cost, 4),
        "answers": rows,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)
    print(f"COMPLETE rows={len(rows)} calls={usage['calls']} failed={usage['failed']} est_cost=${cost:.4f}", flush=True)



if __name__ == "__main__":
    main()
