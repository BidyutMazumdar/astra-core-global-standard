import numpy as np
import json
import os

# ==============================
# CONFIGURATION
# ==============================

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

NUM_ITERATIONS = 10000

VARIABLES = [
    "cyber_stability",
    "ai_governance",
    "legal_coherence",
    "economic_resilience",
    "social_stability"
]

MEANS = np.array([0.85, 0.82, 0.84, 0.83, 0.80])
STDS = np.array([0.08, 0.07, 0.06, 0.09, 0.10])

BOUNDS = np.array([
    [0.40, 1.00],
    [0.45, 1.00],
    [0.50, 1.00],
    [0.40, 1.00],
    [0.35, 1.00]
])

CORRELATION_MATRIX = np.array([
    [1.00, 0.30, 0.35, 0.45, 0.40],
    [0.30, 1.00, 0.55, 0.40, 0.35],
    [0.35, 0.55, 1.00, 0.50, 0.45],
    [0.45, 0.40, 0.50, 1.00, 0.60],
    [0.40, 0.35, 0.45, 0.60, 1.00]
])

WEIGHTS = np.array([0.25, 0.20, 0.20, 0.20, 0.15])

# 🔒 Path Stability Fix
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "outputs", "simulation_results.json")


# ==============================
# INPUT VALIDATION (Audit-grade)
# ==============================

def validate_inputs():
    # Weights check
    if not np.isclose(np.sum(WEIGHTS), 1.0):
        raise ValueError("Weights must sum to 1")

    # Symmetry check
    if not np.allclose(CORRELATION_MATRIX, CORRELATION_MATRIX.T):
        raise ValueError("Correlation matrix must be symmetric")

    # Positive definiteness check
    eigvals = np.linalg.eigvals(CORRELATION_MATRIX)
    if np.any(eigvals <= 0):
        raise ValueError("Correlation matrix must be positive definite")


# ==============================
# SAFEGUARD: Covariance Matrix
# ==============================

def compute_covariance_matrix(stds, corr_matrix):
    return np.outer(stds, stds) * corr_matrix


def stable_cholesky(cov_matrix):
    try:
        return np.linalg.cholesky(cov_matrix)
    except np.linalg.LinAlgError:
        eigvals, eigvecs = np.linalg.eigh(cov_matrix)
        eigvals[eigvals < 1e-6] = 1e-6
        cov_matrix_fixed = eigvecs @ np.diag(eigvals) @ eigvecs.T
        return np.linalg.cholesky(cov_matrix_fixed)


# ==============================
# SCENARIO HOOK
# ==============================

def apply_scenario_adjustment(samples, scenario=None):
    return samples


# ==============================
# SAMPLING FUNCTION
# ==============================

def generate_samples():
    cov_matrix = compute_covariance_matrix(STDS, CORRELATION_MATRIX)
    L = stable_cholesky(cov_matrix)

    Z = np.random.normal(size=(NUM_ITERATIONS, len(VARIABLES)))
    samples = Z @ L.T + MEANS

    # Bounds enforcement
    for i in range(len(VARIABLES)):
        samples[:, i] = np.clip(samples[:, i], BOUNDS[i][0], BOUNDS[i][1])

    # NaN protection
    samples = np.nan_to_num(samples)

    return samples


# ==============================
# DECISION SCORE
# ==============================

def compute_decision_score(samples):
    return np.dot(samples, WEIGHTS)


# ==============================
# RISK CLASSIFICATION
# ==============================

def classify_risk(score):
    if score > 0.75:
        return "Low Risk"
    elif score > 0.60:
        return "Moderate Risk"
    else:
        return "High Risk"


# ==============================
# SAVE OUTPUT
# ==============================

def save_output(result):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=4)


# ==============================
# MAIN SIMULATION
# ==============================

def run_simulation(scenario=None):
    # 🔒 Validation Layer
    validate_inputs()

    samples = generate_samples()
    samples = apply_scenario_adjustment(samples, scenario)

    scores = compute_decision_score(samples)

    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_dev = np.std(scores)

    ci_lower = np.percentile(scores, 5)
    ci_upper = np.percentile(scores, 95)

    low = np.mean(scores > 0.75)
    moderate = np.mean((scores > 0.60) & (scores <= 0.75))
    high = np.mean(scores <= 0.60)

    extreme_prob = np.mean(scores < 0.60)

    result = {
        "decision_integrity_score": float(mean_score),
        "median": float(median_score),
        "std_dev": float(std_dev),
        "confidence_interval": {
            "lower": float(ci_lower),
            "upper": float(ci_upper)
        },
        "risk_probabilities": {
            "low": float(low),
            "moderate": float(moderate),
            "high": float(high)
        },
        "tail_risk_probability": float(extreme_prob),
        "risk_classification": classify_risk(mean_score),

        "metadata": {
            "num_iterations": NUM_ITERATIONS,
            "random_seed": RANDOM_SEED
        }
    }

    return result


# ==============================
# EXECUTION
# ==============================

if __name__ == "__main__":
    output = run_simulation()

    print("\n=== ASTRA CORE Simulation Output ===\n")
    for k, v in output.items():
        print(f"{k}: {v}")

    save_output(output)
