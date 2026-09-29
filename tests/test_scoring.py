import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main as screener  # noqa: E402

GOOD = {
    "ticker": "VNET", "direction": "long",
    "market_missing": "Market prices a contracted infrastructure business as a leveraged macro bet.",
    "catalyst": "Contract acceleration Q2", "invalidation": "Export ban or execution failure",
    "conviction": 7.0, "non_consensus": "y", "near_catalyst": "y", "liquid": "y",
    "win_loss_ratio": 2.5, "fundamental_model": "y", "pitched": "n",
}


def score(**over):
    return screener.score_idea({**GOOD, **over})


class Scoring(unittest.TestCase):
    def test_default_example(self):
        r = score()
        self.assertEqual(r["score"], 85)
        self.assertTrue(r["rating"].startswith("PUBLISH-READY"))

    def test_maximum_is_100(self):
        self.assertEqual(score(conviction=9, win_loss_ratio=3.5, pitched="y")["score"], 100)

    def test_clamped_at_zero(self):
        r = score(non_consensus="n", near_catalyst="n", fundamental_model="n", win_loss_ratio=1.0,
                  conviction=2, liquid="n", market_missing="", invalidation="")
        self.assertEqual(r["score"], 0)
        self.assertTrue(r["rating"].startswith("NOT READY"))

    def test_missing_thesis_text_is_penalised(self):
        self.assertEqual(score()["score"] - score(market_missing="short")["score"], 10)
        self.assertEqual(score()["score"] - score(invalidation="")["score"], 5)

    def test_risk_reward_thresholds(self):
        self.assertEqual(score(win_loss_ratio=3.0)["score"] - score(win_loss_ratio=2.0)["score"], 8)
        self.assertEqual(score(win_loss_ratio=1.49)["score"], score(win_loss_ratio=0.5)["score"])


if __name__ == "__main__":
    unittest.main()
