"""Golden tests for the checklist scorer (added Oct 28, 2026).

The scorer is deterministic and standard-library only, so its output on
the frozen 48 questions must reproduce the committed scores exactly:
same counts, same flags on the same questions. Run from the repo root:

    python3 -m unittest discover -s src
"""

import importlib.util
import json
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "audit_questions", Path(__file__).parent / "audit_questions.py")
aq = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aq)


def flag_pairs(result):
    return sorted((f["code"], f["level"]) for f in result["flags"])


class ScorerGoldenTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = json.loads(
            (REPO / "data" / "questions.json").read_text(encoding="utf-8"))
        cls.committed = json.loads(
            (REPO / "data" / "question_scores.json").read_text(encoding="utf-8"))
        cls.fresh = [aq.score_question(q) for q in cls.questions]

    def test_question_count(self):
        self.assertEqual(len(self.fresh), 48)
        self.assertEqual(len(self.committed), 48)

    def test_headline_counts(self):
        any_flag = [r for r in self.fresh if r["flags"]]
        self.assertEqual(len(any_flag), 31)
        codes = Counter(f["code"] for r in self.fresh for f in r["flags"])
        self.assertEqual(codes["PAST_DATE"], 5)
        self.assertEqual(codes["NO_SOURCE_CUE"], 9)
        self.assertEqual(codes["NUMERIC_CLAIM_REVIEW"], 21)
        flag_level = [r for r in self.fresh
                      if any(f["level"] == "FLAG" for f in r["flags"])]
        self.assertEqual(len(flag_level), 14)

    def test_flags_match_committed_scores(self):
        committed_by_id = {r["id"]: r for r in self.committed}
        for result in self.fresh:
            self.assertIn(result["id"], committed_by_id)
            self.assertEqual(
                flag_pairs(result),
                flag_pairs(committed_by_id[result["id"]]),
                f"flags differ for {result['id']}")


if __name__ == "__main__":
    unittest.main()
