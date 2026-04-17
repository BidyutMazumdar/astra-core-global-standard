# ASTRA CORE Sovereign Simulation System  
## Engine Specification — Scenario-Orchestrated Monte Carlo Execution  

---

## 1. Overview  

The ASTRA CORE Simulation Engine is a probabilistic sovereign decision system that integrates:  

- Multi-scenario modeling  
- Correlated stochastic simulation (Monte Carlo)  
- Risk aggregation and classification  
- Uncertainty propagation and robustness analysis  

This document defines how all scenarios are orchestrated and executed within a unified simulation framework.  

---

## 2. System Architecture  

The execution pipeline follows a layered architecture:  

1. Scenario Layer  
2. Simulation Engine Layer  
3. Aggregation Layer  
4. Output Intelligence Layer  

Each layer operates deterministically under a controlled probabilistic framework.  

---

## 3. Scenario Integration Model  

### 3.1 Scenario Registry  

The system supports the following scenarios:  

- Baseline (Control)  
- Cyber Attack  
- War (Systemic Shock)  
- Economic Crisis  
- Social Instability  

Each scenario is defined as a structured JSON file and mapped to system variables.  

---

### 3.2 Scenario Execution Mapping  

Each scenario modifies system behavior through:  

- Target variables  
- Impact type (direct / cascading / systemic)  
- Execution mode  

| Scenario | Impact Scope | Type |
|----------|-------------|------|
| Cyber Attack | Cyber Stability | Direct |
| War | All variables | Systemic |
| Economic Crisis | Economic + Social | Cascading |
| Social Instability | Social + Legal | Feedback Loop |

---

### 3.3 Scenario Weighting  

\[
P(total) = \sum_{i=1}^{n} w_i \cdot S_i
\]

Where:  

- \( w_i \) = scenario weight  
- \( S_i \) = scenario outcome distribution  

Constraint:  

\[
\sum w_i = 1
\]

---

### 3.4 Scenario Interaction Model  

\[
S_{combined} = \max(S_i) + \sum_{j \neq i} \alpha_j S_j
\]

Where:  

- \( S_i \) = dominant scenario  
- \( \alpha_j \) = attenuation factor (0 < α < 1)  

Rules:  

- Systemic shocks take precedence  
- Secondary shocks are attenuated  
- Conflict resolved via dominance  
- Nonlinear superposition applied  

---

## 4. Monte Carlo Simulation Engine  

### 4.1 Correlated Sampling  

\[
X \sim \mathcal{N}(\mu, \Sigma)
\]

\[
\Sigma = D \cdot R \cdot D
\]

---

### 4.2 Cholesky Decomposition  

\[
X = ZL^T + \mu
\]

Fallback: Eigenvalue decomposition  

---

### 4.3 Bounded Sampling  

\[
X_i \in [lower_i, upper_i]
\]

Method: Hard clipping  

---

## 5. Execution Pipeline  

1. Validate inputs  
2. Load scenarios  
3. Generate baseline samples  
4. Apply scenario adjustments  
5. Inject shocks  
6. Compute scores  
7. Aggregate results  
8. Compute risks  
9. Generate outputs  

---

## 6. Decision Model  

\[
D = 0.25C + 0.20A + 0.20L + 0.20E + 0.15S
\]

---

## 7. Risk Classification  

| Range | Risk |
|------|------|
| > 0.75 | Low |
| 0.60 – 0.75 | Moderate |
| < 0.60 | High |

---

## 8. Uncertainty Propagation  

- Distribution tracking  
- Confidence intervals (5–95)  
- Tail risk estimation  

---

## 9. Shock Injection  

- Probabilistic trigger  
- Uniform intensity  
- Nonlinear superposition  

---

## 10. Output Metrics  

- Decision score  
- Risk distribution  
- Tail risk  
- Confidence intervals  
- Scenario contributions  

---

## 11. Reproducibility  

- Fixed seed  
- Deterministic execution  
- Full traceability  
- Input validation  

---

## 12. Execution Guarantees  

- Numerical stability  
- Bounded outputs  
- No NaN propagation  
- Edge-case robustness  

---

## 13. System Role  

Probabilistic sovereign decision intelligence core  

---

## 14. Future Extensions  

- API integration  
- Dashboard  
- Bayesian updates  
- Temporal dynamics  

---

## 15. Execution Interface Contract  

### 15.1 Input Schema  

- Scenario weights  
- Distribution parameters  
- Correlation matrix  
- Simulation parameters  

---

### 15.2 Execution Contract  

- Deterministic execution  
- Bounded outputs  
- Numerical stability  
- Full traceability  

---

### 15.3 Output Schema  

```json
{
  "decision_integrity_score": "float",
  "confidence_interval": {
    "lower": "float",
    "upper": "float"
  },
  "risk_classification": "string",
  "scenario_contributions": {
    "baseline": "float",
    "cyber_attack": "float",
    "economic_crisis": "float",
    "social_instability": "float",
    "war": "float"
  },
  "tail_risk_probability": "float",
  "stability_index": "float"
}
```

---

### 15.4 System Compatibility  

- Python (NumPy)  
- REST API ready  
- Dashboard compatible  

---
