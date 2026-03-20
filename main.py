"""
Aeon Investment Idea Screener
==============================
Score an investment thesis before committing model-building time.

The seven dimensions measured:
  1. Non-consensus signal     (0/10/25 pts)
  2. Near-term catalyst       (5/20 pts)
  3. Fundamental model        (0/8/20 pts)
  4. Risk/reward ratio        (0/5/12/20 pts)
  5. Conviction level         (0/4/8 pts)
  6. Liquidity adequacy       (0/4 pts)
  7. Stress-tested            (0/3 pts)
  Penalties: unclear mispricing (-10), no invalidation (-5)

Score 0–100. Output: rating, strengths, flags, next steps.

LiJie Guo · Aeon Nimbus Research · lijieguo.substack.com
Dependencies: Python standard library only
"""

import os
import sys


# ---------------------------------------------------------------------------
# DISPLAY HELPERS
# ---------------------------------------------------------------------------

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def separator(char="─", width=66):
    print("  " + char * width)


def header(title: str):
    print()
    separator("═")
    print(f"  {title}")
    separator("═")
    print()


def prompt(label: str, default: str = "") -> str:
    """Prompt with default shown in brackets."""
    if default:
        user = input(f"  {label}\n  [{default}]: ").strip()
        return user if user else default
    else:
        user = input(f"  {label}: ").strip()
        return user


def prompt_float(label: str, default: float, lo: float = 0.0, hi: float = 1e9) -> float:
    """Numeric prompt with validation."""
    while True:
        raw = input(f"  {label} [{default}]: ").strip()
        if not raw:
            return default
        try:
            val = float(raw)
            if lo <= val <= hi:
                return val
            print(f"  [!] Enter a value between {lo} and {hi}.")
        except ValueError:
            print("  [!] Please enter a number.")


def prompt_choice(label: str, options: dict, default: str) -> str:
    """
    Prompt with labelled options dict e.g. {'y': 'Yes', 'n': 'No'}.
    Returns the chosen key.
    """
    opts_str = " / ".join(f"{k}={v}" for k, v in options.items())
    while True:
        raw = input(f"  {label}\n  ({opts_str}) [{default}]: ").strip().lower()
        if not raw:
            return default
        if raw in options:
            return raw
        print(f"  [!] Enter one of: {', '.join(options.keys())}")


def score_bar(score: int, width: int = 40) -> str:
    filled = round(score / 100 * width)
    empty = width - filled
    return "[" + "█" * filled + "░" * empty + "]"


# ---------------------------------------------------------------------------
# SCORING ENGINE
# ---------------------------------------------------------------------------

def score_idea(inputs: dict) -> dict:
    """
    Apply the scoring model to the inputs dict.
    Returns dict with score, rating, strengths, flags.
    """
    score = 0
    strengths = []
    flags = []

    nc       = inputs["non_consensus"]       # y / partial / n
    near     = inputs["near_catalyst"]       # y / n
    fund     = inputs["fundamental_model"]   # y / m / n
    wl       = inputs["win_loss_ratio"]
    conv     = inputs["conviction"]
    liq      = inputs["liquid"]              # y / n
    pitched  = inputs["pitched"]             # y / n
    miss_txt = inputs["market_missing"]
    inv_txt  = inputs["invalidation"]

    # ── 1. Non-consensus signal ─────────────────────────────────────────────
    if nc == "y":
        score += 25
        strengths.append("Genuinely non-consensus — maximum differentiation from consensus")
    elif nc == "partial":
        score += 10
        flags.append("Only partially non-consensus — what is the specific edge vs the street?")
    else:  # n
        score += 0
        flags.append("Consensus view — you have no informational or analytical edge here. Pass.")

    # ── 2. Near-term catalyst ───────────────────────────────────────────────
    if near == "y":
        score += 20
        strengths.append("Near-term catalyst defines the P&L timeline")
    else:
        score += 5
        flags.append(
            "No near-term catalyst — a great thesis can take years to play out, "
            "which is expensive in opportunity cost"
        )

    # ── 3. Fundamental model support ────────────────────────────────────────
    if fund == "y":
        score += 20
        strengths.append("Fundamental model confirms the thesis — numbers support the story")
    elif fund == "m":
        score += 8
        flags.append(
            "Mixed fundamentals — the model needs to clearly support the thesis before publishing"
        )
    else:  # n
        score += 0
        flags.append(
            "Qualitative only — do not publish without a model. "
            "This is not an investment thesis, it is a hypothesis."
        )

    # ── 4. Risk/reward ratio ────────────────────────────────────────────────
    if wl >= 3.0:
        score += 20
        strengths.append(f"Excellent risk/reward ({wl:.1f}x) — asymmetric payoff")
    elif wl >= 2.0:
        score += 12
        strengths.append(f"Adequate risk/reward ({wl:.1f}x) — meets minimum threshold")
    elif wl >= 1.5:
        score += 5
        flags.append(
            f"Marginal risk/reward ({wl:.1f}x) — acceptable only with very high win probability"
        )
    else:
        score += 0
        flags.append(f"Poor risk/reward (<1.5x) — risk is not worth taking at this ratio")

    # ── 5. Conviction ────────────────────────────────────────────────────────
    if conv >= 8:
        score += 8
        strengths.append(f"High conviction ({int(conv)}/10)")
    elif conv >= 5:
        score += 4
        # no flag, no strength displayed — neutral
    else:
        score += 0
        flags.append(
            f"Low conviction ({int(conv)}/10) — do more work before committing to this publicly"
        )

    # ── 6. Liquidity ─────────────────────────────────────────────────────────
    if liq == "y":
        score += 4
        strengths.append("Adequate liquidity for position entry and exit")
    else:
        score += 0
        flags.append("Illiquidity risk — size this smaller than your model would suggest")

    # ── 7. Stress-tested ─────────────────────────────────────────────────────
    if pitched == "y":
        score += 3
        strengths.append("Stress-tested — critical feedback has been incorporated")
    else:
        score += 0
        flags.append(
            "Not yet stress-tested — find one person who disagrees "
            "and hear them out before publishing"
        )

    # ── Penalties ─────────────────────────────────────────────────────────────
    if not miss_txt or len(miss_txt.strip()) < 20:
        score -= 10
        flags.append(
            "Mispricing not clearly articulated — this is the core of the thesis. "
            "If you cannot state what the market is missing in 2 sentences, the idea is not ready."
        )

    if not inv_txt or len(inv_txt.strip()) < 10:
        score -= 5
        flags.append(
            "Invalidation condition not specified — "
            "every thesis needs a stated reason to close the position"
        )

    # Clamp
    score = max(0, min(100, score))

    # Rating
    if score >= 75:
        rating = "PUBLISH-READY — Strong idea"
        rating_sym = "✓✓✓"
    elif score >= 50:
        rating = "DEVELOPING — Address the flags before publishing"
        rating_sym = "⚠⚠"
    else:
        rating = "NOT READY — Significant gaps in the thesis"
        rating_sym = "✗✗"

    # Actionable next steps based on flags
    next_steps = _derive_next_steps(flags, score)

    return {
        "score": score,
        "rating": rating,
        "rating_sym": rating_sym,
        "strengths": strengths,
        "flags": flags,
        "next_steps": next_steps,
    }


def _derive_next_steps(flags: list, score: int) -> str:
    """Generate 1-2 sentences of actionable guidance based on the flags."""
    if score >= 75:
        return (
            "The thesis is publish-ready. Refine the catalyst timeline, "
            "set a hard invalidation price, and finalize position sizing before publishing."
        )

    priority = []
    for flag in flags:
        if "Qualitative only" in flag or "without a model" in flag:
            priority.append("Build the financial model before publishing — qualitative analysis alone does not constitute an investment thesis.")
        elif "non-consensus" in flag and "Consensus view" in flag:
            priority.append("If the view is consensus, the risk/reward is not there — find the specific differentiated insight or move on.")
        elif "mispricing" in flag.lower() or "Mispricing" in flag:
            priority.append("Write one crisp sentence stating exactly what the market is pricing incorrectly and why you are right.")
        elif "catalyst" in flag.lower():
            priority.append("Identify the specific near-term catalyst that will close the gap between price and value — without one, the idea may be correct but early.")
        elif "Invalidation" in flag:
            priority.append("Define your invalidation condition before entering — know precisely what would make you wrong and close the position.")
        elif "risk/reward" in flag.lower():
            priority.append("Re-examine the target and stop levels — the R-multiple must be at least 2.0 before committing capital.")
        elif "stress-tested" in flag.lower() or "Stress-tested" in flag:
            priority.append("Find a credible bear on this name and stress-test the thesis against their best arguments.")

    # Return top 2 unique actions
    seen = set()
    unique = []
    for p in priority:
        if p not in seen:
            seen.add(p)
            unique.append(p)
        if len(unique) == 2:
            break

    if not unique:
        return "Review the flagged items above and iterate on the thesis before allocating capital."

    return " ".join(unique)


# ---------------------------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------------------------

def display_results(inputs: dict, result: dict):
    """Render the scoring output."""
    clear()
    header("AEON INVESTMENT IDEA SCREENER — RESULTS")

    score = result["score"]
    bar = score_bar(score)

    # Score box
    print(f"  SCORE:  {score:3d} / 100   {bar}")
    print()
    print(f"  Rating: {result['rating_sym']}  {result['rating']}")
    separator()
    print(f"  Trade:  {inputs['direction'].upper()} {inputs['ticker'].upper()}")
    if inputs['catalyst']:
        print(f"  Catalyst:      {inputs['catalyst']}")
    if inputs['invalidation']:
        print(f"  Invalidation:  {inputs['invalidation']}")
    separator()

    # Strengths
    if result["strengths"]:
        print()
        print("  STRENGTHS:")
        for i, s in enumerate(result["strengths"], 1):
            print(f"    {i}. ✓  {s}")

    # Flags
    if result["flags"]:
        print()
        print("  FLAGS / WARNINGS:")
        for i, f in enumerate(result["flags"], 1):
            print(f"    {i}. ⚠  {f}")

    # Next steps
    print()
    separator()
    print("  RECOMMENDED NEXT STEPS:")
    print()
    # Wrap at ~65 chars
    words = result["next_steps"].split()
    line = "  "
    for word in words:
        if len(line) + len(word) + 1 > 68:
            print(line)
            line = "    " + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

    print()
    separator("═")
    print(f"  Aeon Nimbus Research · lijieguo.substack.com")
    separator("═")
    print()


# ---------------------------------------------------------------------------
# COLLECT INPUTS
# ---------------------------------------------------------------------------

def collect_inputs() -> dict:
    """Interactive input collection with defaults."""
    clear()
    header("AEON INVESTMENT IDEA SCREENER — INPUTS")

    print("  Press Enter to accept the default value shown in [brackets].")
    print("  Example filled with VNET Group long thesis.")
    print()

    ticker     = prompt("Ticker", "VNET").upper()
    direction  = prompt_choice(
        "Direction",
        {"long": "Long", "short": "Short"},
        "long"
    )

    print()
    separator()
    print("  THESIS QUALITY")
    separator()

    market_missing = prompt(
        "What is the market missing? (mispricing in 1–2 sentences)",
        "Market pricing VNET as a leveraged China macro bet. It is a contracted "
        "infrastructure business — 98.7% pre-commitment rates, 9-12 month delivery "
        "vs 14-18 month industry average."
    )

    catalyst = prompt(
        "Primary catalyst and timing",
        "ByteDance 100MW contract acceleration — Q2 2026"
    )

    invalidation = prompt(
        "What makes you wrong? (invalidation condition)",
        "Permanent GPU export ban OR management execution failure"
    )

    conviction = prompt_float("Conviction level (1–10)", 7.0, 1, 10)

    print()
    separator()
    print("  SCREENING CRITERIA")
    separator()

    non_consensus = prompt_choice(
        "Is the thesis genuinely non-consensus?",
        {"y": "Yes — street is wrong", "partial": "Partially — mixed signals", "n": "No — consensus"},
        "y"
    )

    near_catalyst = prompt_choice(
        "Is the primary catalyst within 6 months?",
        {"y": "Yes — near-term", "n": "No — longer dated"},
        "y"
    )

    liquid = prompt_choice(
        "Is the stock sufficiently liquid to exit quickly?",
        {"y": "Yes — large/mid cap", "n": "No — small/illiquid"},
        "y"
    )

    win_loss = prompt_float(
        "Upside / downside ratio (estimated, e.g. 2.5 means 2.5x upside vs 1x downside)",
        2.5, 0.1, 20.0
    )

    fundamental = prompt_choice(
        "Does the fundamental model confirm the thesis?",
        {"y": "Yes — numbers support", "m": "Partial — mixed signals", "n": "Not yet — qualitative only"},
        "y"
    )

    pitched = prompt_choice(
        "Has this idea been pitched to a critical audience?",
        {"y": "Yes — stress-tested", "n": "No — first pass"},
        "n"
    )

    return {
        "ticker": ticker,
        "direction": direction,
        "market_missing": market_missing,
        "catalyst": catalyst,
        "invalidation": invalidation,
        "conviction": conviction,
        "non_consensus": non_consensus,
        "near_catalyst": near_catalyst,
        "liquid": liquid,
        "win_loss_ratio": win_loss,
        "fundamental_model": fundamental,
        "pitched": pitched,
    }


# ---------------------------------------------------------------------------
# BATCH MODE — score multiple ideas, compare
# ---------------------------------------------------------------------------

def compare_mode():
    """Screen multiple ideas and display a ranked summary."""
    ideas = []
    while True:
        clear()
        header("AEON IDEA SCREENER — COMPARISON MODE")
        if ideas:
            print(f"  {len(ideas)} idea(s) screened so far:")
            for idx, (inp, res) in enumerate(ideas, 1):
                bar = score_bar(res["score"], width=20)
                print(f"    {idx}. {inp['ticker']:6s} {inp['direction'].upper():5s}  "
                      f"{res['score']:3d}/100  {bar}  {res['rating'][:30]}")
            print()

        choice = input(
            "  [A] Add another idea   [V] View detail   [Q] Quit comparison\n  > "
        ).strip().lower()

        if choice == "a":
            inp = collect_inputs()
            res = score_idea(inp)
            ideas.append((inp, res))
            display_results(inp, res)
            input("  Press Enter to continue...")

        elif choice == "v" and ideas:
            num = input(f"  View which idea? (1–{len(ideas)}): ").strip()
            try:
                idx = int(num) - 1
                if 0 <= idx < len(ideas):
                    display_results(*ideas[idx])
                    input("  Press Enter to continue...")
            except ValueError:
                pass

        elif choice in ("q", "quit", "exit"):
            if ideas:
                # Print ranked summary
                clear()
                header("COMPARISON SUMMARY — RANKED BY SCORE")
                ranked = sorted(ideas, key=lambda x: x[1]["score"], reverse=True)
                for rank, (inp, res) in enumerate(ranked, 1):
                    bar = score_bar(res["score"], width=25)
                    print(f"  #{rank}  {inp['ticker']:6s} {inp['direction'].upper():5s}  "
                          f"{res['score']:3d}/100  {bar}")
                    print(f"       {res['rating']}")
                    if res["strengths"]:
                        print(f"       Top strength: {res['strengths'][0]}")
                    if res["flags"]:
                        print(f"       Top flag:     {res['flags'][0]}")
                    print()
                input("  Press Enter to exit...")
            break


# ---------------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------------

def main():
    while True:
        clear()
        header("AEON INVESTMENT IDEA SCREENER")
        print("  Score a thesis before committing model-building time.")
        print("  Seven dimensions. One score. Clear next steps.")
        print()
        print("  1.  Screen a single idea")
        print("  2.  Compare multiple ideas (ranked)")
        print("  0.  Exit")
        print()

        choice = input("  Select [0–2]: ").strip()

        if choice == "0":
            print("\n  Aeon Nimbus Research — goodbye.\n")
            sys.exit(0)

        elif choice == "1":
            inputs = collect_inputs()
            result = score_idea(inputs)
            display_results(inputs, result)
            input("  Press Enter to return to menu...")

        elif choice == "2":
            compare_mode()

        else:
            print("  [!] Invalid choice. Enter 0, 1, or 2.")
            input("  Press Enter...")


if __name__ == "__main__":
    main()
