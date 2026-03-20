# Aeon Investment Idea Screener

**Thesis Quality · Non-Consensus Signal · Catalyst Timing · Publishability Score**

*LiJie Guo · Aeon Nimbus Research · lijieguo.substack.com · [LinkedIn](https://www.linkedin.com/in/lijieguo-es/)*

---

## Overview

The most expensive research asset in institutional investing is analyst time — and most of it is spent building models on ideas that do not survive first-principles scrutiny. The Aeon Idea Screener is the pre-filter applied before that commitment: a structured seven-dimension scoring framework that asks the same questions a portfolio manager applies in the first sixty seconds of hearing a pitch. A thesis that cannot answer these questions quantitatively, with specific and falsifiable responses, does not justify a full model build.

```bash
# Score a single idea, or score and rank multiple in comparison
python main.py
```

Python 3.8 or later. No external dependencies.

---

## Scoring Model

Seven dimensions, scored from 0 to 100 in aggregate:

| Dimension | Weight | Core Question |
|-----------|--------|---------------|
| Non-consensus signal | 25 pts | What does the market not yet reflect that you can articulate precisely? |
| Near-term catalyst | 20 pts | What specific event will surface the mispricing, and on what timeline? |
| Fundamental model support | 20 pts | Do the numbers independently confirm the qualitative thesis? |
| Risk/reward ratio | 20 pts | Is the upside asymmetry at minimum 2× the downside on a through-cycle view? |
| Conviction | 8 pts | How confident are you in the thesis, honestly and ex-ante? |
| Liquidity | 4 pts | Is there sufficient market depth to enter and exit at the intended size? |
| Stress-tested | 3 pts | Has a credible opponent made their best case against you? |
| *Penalties* | up to −15 | Unclear or absent mispricing logic; missing invalidation condition |

**Score interpretation:**
- **75–100:** Publish-ready — the thesis has identifiable edge, near-term testability, and analytical rigour
- **50–74:** Developing — specific gaps exist that are addressable before publishing
- **0–49:** Not ready — structural weaknesses in the thesis; return to first principles

---

## Methodology

### Non-Consensus as the Necessary Condition for Alpha

In a semi-strong efficient market, prices incorporate all publicly available information. Excess risk-adjusted returns can therefore only arise from one of three sources: information the market does not have, analysis the market has not done, or a behavioural bias the market is systematically committing. A view that coincides with consensus is not a trade — it is a description of the current price. This is why the non-consensus dimension carries the highest weight in the scoring model. Without a clearly articulable differentiation from the street's prevailing view, there is no rational basis for a position from a risk-adjusted returns perspective, regardless of how well the model is constructed.

The quality of the non-consensus claim matters as much as its existence. "I think the stock is undervalued" is not non-consensus; it is a directional preference. "The market is attributing no value to the hyperscale data centre pipeline because sell-side models use legacy colocation multiples and miss the structural demand inflection from GPU compute buildout" is non-consensus — specific, falsifiable, and actionable.

### The Catalyst as the P&L Timeline

Being right too early is economically equivalent to being wrong. A thesis that requires three years for the market to recognise incurs three years of mark-to-market risk, opportunity cost, and capital at risk against a benchmark that may deliver positive returns over that same period. The catalyst is the mechanism by which the market's view converges to yours on a defined timeline.

A concrete catalyst also disciplines ongoing position management. If the catalyst occurs and the stock does not respond, this is data: either the thesis is wrong, the market requires a second catalyst, or the mispricing is structural and will take longer to close. This prevents the analytically common but intellectually dishonest pattern of rationalising away negative price action as "the market being irrational" without a specific explanation of when and why it will stop being irrational.

### R-Multiple as the Minimum Viability Filter

The reward-to-risk ratio connects directly to the expected value framework underlying the Kelly Criterion. For a trade with win probability p and R-multiple R:

```
Expected value per trade = p × R − (1−p) × 1
```

At a realistic fundamental equity win rate of 40% — representative of a disciplined, well-researched process — the minimum R required for positive expectancy is:

```
E[V] > 0  ⟹  0.40 × R > 0.60  ⟹  R > 1.5
```

The professional standard of R ≥ 2.0 provides a margin of safety against win rate estimation error. Below this threshold, a positive-expectancy strategy requires win rates above 50%, which are empirically difficult to sustain across a diversified book of fundamental ideas. The R-minimum is not a conservative preference; it is a mathematical constraint on any strategy that compounds over multiple positions.

### Thesis Invalidation as Epistemic Discipline

An investment thesis without a stated invalidation condition is not a thesis — it is a directional commitment with no exit logic. The invalidation condition serves three functions. First, it specifies the observable outcome that would falsify the thesis, distinguishing genuine adverse signal from temporary market noise. Second, it anchors the stop-loss framework: position management becomes systematic when there is a pre-defined trigger for closure. Third, it forces the analyst to engage seriously with the bear case before capital is deployed rather than constructing that case retroactively when the position is moving against them.

The absence of an invalidation condition is one of the most reliable markers of confirmation bias in investment research. Its presence is one of the markers of a disciplined investment process.

### Adversarial Stress-Testing

Lovallo and Kahneman's research on planning fallacy and the inside-view bias demonstrates that individual forecasters systematically underestimate downside risk by anchoring too strongly to their own mental models and too weakly to the base rate of comparable situations. The antidote is structured adversarial engagement: pitching the idea to a credible bear — someone who knows the security well and disagrees — before committing capital. The goal is not to be talked out of the position but to ensure the best case against the thesis has been heard and addressed. Ideas that survive this process are materially stronger than those that have not.

---

## Why This Matters

Institutional equity research is a time-constrained operation. A mid-cap initiating coverage report consumes 40–80 analyst hours before a single word is published. The economic cost of committing that resource to an idea that fails basic pre-screening is substantial — and avoidable. The questions in this screener are not novel; they are the standard questions applied by Tiger Cubs, multi-manager pod PMs, and senior equity analysts across the industry. The discipline of requiring answers before building the model — rather than discovering the answers' absence after completing it — is the difference between process-driven research and effort-intensive wishful thinking.

The highest-alpha analysts in this industry are not distinguished by the volume of ideas they generate. They are distinguished by the ruthlessness with which they filter ideas before committing resources, and the clarity with which they state what would cause them to change their mind.

---

## Example Output

```
════════════════════════════════════════════════════════════════
  AEON INVESTMENT IDEA SCREENER — RESULTS
════════════════════════════════════════════════════════════════

  SCORE:   74 / 100   [██████████████████████████████░░░░░░░░░░]

  Rating:  DEVELOPING — Address identified gaps before publishing

  Trade:       LONG VNET
  Catalyst:    ByteDance 100MW contract acceleration — Q2 2026
  Invalidation: Permanent GPU export restriction  OR
                Sustained management execution failure (3 consecutive
                quarters of guidance miss)

  ─────────────────────────────────────────────────────────────
  STRENGTHS:
    ✓  Genuinely non-consensus — differentiated from sell-side consensus
    ✓  Near-term catalyst defines the P&L timeline and thesis test
    ✓  Fundamental model independently confirms the thesis
    ✓  Risk/reward ratio of 2.5× meets minimum threshold
    ✓  High conviction (8/10) appropriately justified by work done
    ✓  Adequate liquidity for intended position size

  FLAGS:
    ⚠  Not yet stress-tested — identify a credible bear and engage
       with their best arguments before publishing or allocating

  ─────────────────────────────────────────────────────────────
  NEXT STEP:
  Find one person who knows VNET well and disagrees with the thesis.
  Hear them out fully. Then either update the thesis or publish with
  the bear case explicitly addressed.

════════════════════════════════════════════════════════════════
  Aeon Nimbus Research · lijieguo.substack.com
════════════════════════════════════════════════════════════════
```

---

*LiJie Guo · Aeon Nimbus Research · lijieguo.substack.com · [LinkedIn](https://www.linkedin.com/in/lijieguo-es/)*
