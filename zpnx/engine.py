"""
ZimNova Pulse Nexus — Core Computation Engine
All models, simulations, and decision logic.
"""
import numpy as np
from scipy.stats import entropy as scipy_entropy

# ── Lithium Intelligence ─────────────────────────────────────────────

def predict_output(ore_grade: float, extraction_volume: float) -> dict:
    """
    Predict lithium output with dynamic efficiency factor.
    Efficiency scales with ore grade: higher grade → better recovery.
    Returns predicted tonnes and the efficiency used.
    """
    # Efficiency: linear map from grade [1.0–5.0] → efficiency [0.60–0.90]
    efficiency = 0.60 + (ore_grade - 1.0) * (0.30 / 4.0)
    predicted = extraction_volume * (ore_grade / 100.0) * efficiency
    return {"predicted_tonnes": predicted, "efficiency": efficiency}


def run_monte_carlo(predicted: float, ore_grade: float, n: int = 10_000) -> np.ndarray:
    """
    Monte Carlo simulation centered on predicted output.
    Uncertainty inversely proportional to ore grade:
      grade 1.0 → 25% CV,  grade 5.0 → 15% CV.
    """
    cv = 0.25 - (ore_grade - 1.0) * (0.10 / 4.0)   # coefficient of variation
    std = predicted * cv
    samples = np.random.normal(loc=predicted, scale=std, size=n)
    return samples[samples > 0]  # physical constraint: no negative output


def calculate_entropy(samples: np.ndarray, n_bins: int = 50) -> dict:
    """
    Shannon-entropy-based confidence score.
    Lower entropy (tighter distribution) → higher confidence.
    Returns score 0-1 and classification.
    """
    counts, _ = np.histogram(samples, bins=n_bins)
    probs = counts / counts.sum()
    probs = probs[probs > 0]
    H = scipy_entropy(probs, base=2)
    H_max = np.log2(n_bins)
    normalised = H / H_max if H_max > 0 else 1.0
    confidence = round(1.0 - normalised, 4)
    if confidence > 0.7:
        classification = "HIGH"
    elif confidence >= 0.4:
        classification = "MEDIUM"
    else:
        classification = "LOW"
    return {"score": confidence, "classification": classification,
            "raw_entropy": round(H, 4)}


# ── Agricultural Credit Engine ───────────────────────────────────────

def predict_yield(rainfall: float, soil_quality: float,
                  historical_yield: float) -> float:
    """
    Weighted yield prediction (tonnes/ha).
    Weights: rainfall 0.40, soil 0.35, historical 0.25.
    Inputs are normalised 0-100 scales.
    """
    w_rain, w_soil, w_hist = 0.40, 0.35, 0.25
    raw = (rainfall * w_rain + soil_quality * w_soil +
           historical_yield * w_hist)
    return round(raw, 2)


def compute_credit_score(predicted_yield: float, confidence: float,
                         risk_factor: float) -> dict:
    """
    Credit Score = (Predicted Yield × Confidence) / Risk Factor
    Clamped to 0-100. Returns score + decision.
    """
    if risk_factor <= 0:
        risk_factor = 0.01
    raw = (predicted_yield * confidence) / risk_factor
    score = round(min(max(raw, 0), 100), 1)
    if score >= 65:
        decision = "APPROVED"
    elif score >= 40:
        decision = "CONDITIONAL"
    else:
        decision = "REJECTED"
    return {"score": score, "decision": decision}


# ── Decision Engine ──────────────────────────────────────────────────

def generate_decision(mc_samples: np.ndarray, confidence: dict,
                      predicted: float, market_price: float) -> list:
    """
    Deterministic recommendation engine.
    Combines Monte Carlo spread, confidence, and output stability.
    Returns list of (icon, recommendation) tuples.
    """
    p10 = float(np.percentile(mc_samples, 10))
    p90 = float(np.percentile(mc_samples, 90))
    spread = (p90 - p10) / predicted if predicted > 0 else 999
    conf = confidence["score"]
    recs = []

    # Primary strategic recommendation
    if conf > 0.7 and spread < 0.5:
        recs.append(("✅", "High output stability + high confidence → "
                      "Proceed with beneficiation at full capacity."))
    elif conf > 0.7 and spread >= 0.5:
        recs.append(("⚠️", "High confidence but wide spread → "
                      "Proceed with hedged extraction; lock forward contracts."))
    elif conf <= 0.7 and spread < 0.5:
        recs.append(("🔄", "Moderate confidence, stable output → "
                      "Run pilot extraction before scaling."))
    else:
        recs.append(("🛑", "Low confidence + wide spread → "
                      "Delay extraction. Improve geological survey data."))

    # Price risk
    revenue_p10 = p10 * market_price
    revenue_p90 = p90 * market_price
    if (revenue_p90 - revenue_p10) / max(revenue_p10, 1) > 0.6:
        recs.append(("💰", f"Revenue range ${revenue_p10:,.0f}–"
                      f"${revenue_p90:,.0f} → Hedge price risk before "
                      "committing extraction capital."))

    # Tokenisation eligibility
    token_eligible = conf > 0.7 and spread < 0.6
    if token_eligible:
        recs.append(("🪙", "Asset meets tokenisation threshold → "
                      "Eligible for digital mineral-backed issuance."))
    else:
        reason = "low confidence" if conf <= 0.7 else "high output variance"
        recs.append(("🚫", f"Not eligible for tokenisation — {reason}. "
                      "Improve data quality or reduce extraction variance."))

    # Financing guidance
    if conf < 0.4:
        recs.append(("📉", "Low data confidence → Delay financing decisions "
                      "and improve input data quality."))

    return recs, token_eligible, spread
