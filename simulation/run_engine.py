# ============================================================
# ASTRA CORE™ Sovereign Simulation System
# Execution Entry Point — run_engine.py
# ABSOLUTE LOCK 🔒🔐 FINAL EDITION (Production + Audit Grade)
# ============================================================

import os
import json
import time
import importlib.util
import numpy as np

# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "index.json")
WEIGHTS_PATH = os.path.join(BASE_DIR, "scenario_weights.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "outputs", "simulation_results.json")

ENGINE_PATH = os.path.join(BASE_DIR, "engine", "astra_core_monte_carlo_engine.py")
VALIDATOR_PATH = os.path.join(BASE_DIR, "validate_output.py")

SCENARIO_DIR = os.path.join(BASE_DIR, "scenarios")


# ============================================================
# MODULE LOADER
# ============================================================

def load_module(module_path, module_name):
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Missing module: {module_path}")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ============================================================
# JSON LOADER
# ============================================================

def load_json(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing required file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# SCENARIO LOADER
# ============================================================

def load_scenarios(registry):
    scenarios = {}
    for name, meta in registry.items():
        path = os.path.join(SCENARIO_DIR, meta["file"])
        scenarios[name] = load_json(path)
    return scenarios


# ============================================================
# VALIDATION HELPERS
# ============================================================

def validate_weights(weights):
    total = sum(weights.values())
    if not np.isclose(total, 1.0, atol=1e-6):
        raise ValueError("Scenario weights must sum to 1.0")


def validate_engine_output_structure(result):
    required_fields = [
        "decision_integrity_score",
        "median",
        "std_dev",
        "confidence_interval",
        "risk_probabilities",
        "tail_risk_probability",
        "risk_classification",
        "metadata"
    ]

    for field in required_fields:
        if field not in result:
            raise ValueError(f"Missing required field: {field}")


def validate_weight_scenario_consistency(weights, scenarios):
    for key in weights:
        if key not in scenarios:
            raise ValueError(f"Weight defined for unknown scenario: {key}")


def compute_scenario_contributions(weights):
    total_weight = sum(weights.values())
    return {k: float(w / total_weight) for k, w in weights.items()}


def compute_stability_index(std_dev):
    value = 1.0 - std_dev
    return float(min(1.0, max(0.0, value)))


# ============================================================
# MAIN EXECUTION
# ============================================================

def run_engine():

    # -------------------------------
    # STEP 1: LOAD CONFIG
    # -------------------------------
    index = load_json(INDEX_PATH)
    weights = load_json(WEIGHTS_PATH)

    validate_weights(weights)

    # -------------------------------
    # STEP 2: LOAD SCENARIOS
    # -------------------------------
    scenarios = load_scenarios(index["scenario_registry"])

    # -------------------------------
    # STEP 3: VALIDATE CONSISTENCY
    # -------------------------------
    validate_weight_scenario_consistency(weights, scenarios)

    # -------------------------------
    # STEP 4: LOAD ENGINE
    # -------------------------------
    engine = load_module(ENGINE_PATH, "astra_engine")

    if not hasattr(engine, "run_simulation"):
        raise AttributeError("Engine missing run_simulation()")

    # -------------------------------
    # STEP 5: RUN ENGINE (DETERMINISTIC)
    # -------------------------------
    seed = 42

    result = engine.run_simulation(
        scenarios=scenarios,
        weights=weights,
        seed=seed
    )

    # -------------------------------
    # STEP 6: STRUCTURE VALIDATION
    # -------------------------------
    validate_engine_output_structure(result)

    if "random_seed" not in result["metadata"]:
        raise ValueError("Missing random_seed in metadata")

    if result["metadata"]["random_seed"] != seed:
        raise ValueError("Seed mismatch: non-deterministic execution detected")

    # -------------------------------
    # STEP 7: ENRICH OUTPUT
    # -------------------------------
    result["scenario_contributions"] = compute_scenario_contributions(weights)
    result["stability_index"] = compute_stability_index(result["std_dev"])

    result["metadata"]["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    result["metadata"]["engine_version"] = "1.0"

    # -------------------------------
    # STEP 8: VALIDATE OUTPUT
    # -------------------------------
    validator = load_module(VALIDATOR_PATH, "validator")

    if not hasattr(validator, "validate_output"):
        raise AttributeError("Validator missing validate_output()")

    validator.validate_output(result)

    # -------------------------------
    # STEP 9: SAVE OUTPUT
    # -------------------------------
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    # -------------------------------
    # FINAL LOG
    # -------------------------------
    print("\n=== ASTRA CORE EXECUTION COMPLETE ===")
    print(f"Decision Score: {result['decision_integrity_score']}")
    print(f"Risk: {result['risk_classification']}")
    print(f"Output Saved → {OUTPUT_PATH}")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_engine()
