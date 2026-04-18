# ============================================================
# ASTRA CORE™ Scoring Engine
# File: /models/astra_score.py
# ABSOLUTE LOCK 🔒🔐 FINAL EDITION
# (Deterministic + Bounded + Audit-Proof + Fully Hardened + Immutable Core)
# ============================================================

import numpy as np
from types import MappingProxyType

# Deterministic: No internal randomness. Fully reproducible given inputs.


# ============================================================
# DEFAULT WEIGHTS (IMMUTABLE CANONICAL)
# ============================================================

DEFAULT_WEIGHTS = MappingProxyType({
    "cyber_stability": 0.25,
    "ai_governance": 0.20,
    "legal_coherence": 0.20,
    "economic_resilience": 0.20,
    "social_stability": 0.15
})


# ============================================================
# VALIDATION LAYER (STRICT + FULL HARDENING)
# ============================================================

def validate_inputs(inputs, weights):

    # STRUCTURE VALIDATION
    for key in weights:
        if key not in inputs:
            raise ValueError(f"Missing input variable: {key}")

    for key in inputs:
        if key not in weights:
            raise ValueError(f"Unexpected input variable: {key}")

    # VALUE VALIDATION
    for key, value in inputs.items():

        if not isinstance(value, (int, float)):
            raise TypeError(f"Invalid type for {key}: must be numeric")

        if not np.isfinite(value):
            raise ValueError(f"Invalid numeric value (NaN/Inf): {key}")

        if not (0.0 <= value <= 1.0):
            raise ValueError(f"Value out of bounds [0,1]: {key}={value}")

    # WEIGHT VALIDATION
    for k, w in weights.items():

        if not isinstance(w, (int, float)):
            raise TypeError(f"Invalid weight type: {k}")

        if not np.isfinite(w):
            raise ValueError(f"Invalid weight (NaN/Inf): {k}")

        if not (0.0 <= w <= 1.0):
            raise ValueError(f"Weight out of bounds [0,1]: {k}={w}")

    total_weight = sum(weights.values())

    # Ultra-safe floating tolerance
    if not np.isclose(total_weight, 1.0, rtol=1e-9, atol=1e-9):
        raise ValueError("Weights must sum to 1.0")


# ============================================================
# CORE SCORING FUNCTION
# ============================================================

def compute_astra_score(inputs, weights=None):

    if weights is None:
        weights = DEFAULT_WEIGHTS
    else:
        # Defensive copy if external weights passed
        weights = dict(weights)

    validate_inputs(inputs, weights)

    score = 0.0
    for key, weight in weights.items():
        score += weight * inputs[key]

    # Clamp for floating safety
    return float(min(1.0, max(0.0, score)))


# ============================================================
# DISTRIBUTION METRICS (STRICT + HARDENED)
# ============================================================

def compute_distribution_metrics(samples):

    samples = np.asarray(samples, dtype=np.float64)

    if samples.size < 2:
        raise ValueError("At least 2 samples required for statistical metrics")

    if not np.all(np.isfinite(samples)):
        raise ValueError("Samples contain NaN/Inf values")

    std = float(np.std(samples, ddof=1))

    # Remove floating noise
    if abs(std) < 1e-12:
        std = 0.0

    return {
        "mean": float(np.mean(samples)),
        "median": float(np.median(samples)),
        "std_dev": std,
        "min": float(np.min(samples)),
        "max": float(np.max(samples))
    }


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def classify_risk(score):

    if not np.isfinite(score):
        raise ValueError("Invalid score value")

    if score >= 0.75:
        return "low_risk"
    elif score >= 0.60:
        return "moderate_risk"
    else:
        return "high_risk"


# ============================================================
# CONFIDENCE INTERVAL (STRICT + HARDENED)
# ============================================================

def compute_confidence_interval(samples, lower=5, upper=95):

    samples = np.asarray(samples, dtype=np.float64)

    if not (0 <= lower < upper <= 100):
        raise ValueError("Invalid percentile bounds")

    if samples.size < 2:
        raise ValueError("At least 2 samples required for confidence interval")

    if not np.all(np.isfinite(samples)):
        raise ValueError("Samples contain NaN/Inf values")

    return {
        "lower": float(np.percentile(samples, lower)),
        "upper": float(np.percentile(samples, upper))
    }


# ============================================================
# FULL PIPELINE FUNCTION
# ============================================================

def full_astra_evaluation(inputs, samples=None, weights=None):

    score = compute_astra_score(inputs, weights)

    result = {
        "decision_integrity_score": score,
        "risk_classification": classify_risk(score)
    }

    if samples is not None:
        stats = compute_distribution_metrics(samples)
        ci = compute_confidence_interval(samples)

        result.update({
            "median": stats["median"],
            "std_dev": stats["std_dev"],
            "confidence_interval": ci
        })

    return result
