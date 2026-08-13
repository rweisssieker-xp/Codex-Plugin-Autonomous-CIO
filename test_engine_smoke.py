import unittest

from engine.decision_intelligence_engine import build_decision_packet, score_decision_readiness


class EngineSmokeTest(unittest.TestCase):
    def test_engine_builds_bounded_decision_scores(self):
        context = {
            "title": "Board prep smoke",
            "facts": ["Budget burn is above plan.", "Security testing is not complete."],
            "assumptions": ["Vendor delivery will recover next month."],
            "risks": ["Board approval could be delayed without evidence."],
            "options": ["Approve with guardrails", "Defer until evidence is complete"],
        }

        packet = build_decision_packet(context)
        scorecard = score_decision_readiness(context)

        self.assertIn("facts", packet)
        self.assertIn("missing_evidence", packet)
        for value in scorecard["scorecard"].values():
            self.assertGreaterEqual(value["value"], 0)
            self.assertLessEqual(value["value"], 100)


if __name__ == "__main__":
    unittest.main()
