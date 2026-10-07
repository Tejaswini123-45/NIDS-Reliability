# NIDS Reliability

Reproducible ML research framework for evaluating Logistic Regression, Random Forest, and XGBoost on CICIDS2017 under temporal and controlled feature-missingness conditions.

See `AGENTS.md` for project constraints and `src/` for the ordered implementation extracted from the source notebook.

## Scientific guardrails
- No fabricated results.
- No fake timestamps.
- Training-only preprocessing; avoid leakage.
- Binary and multiclass experiments remain separate.
- Final paper-mode experiments require seeds 42, 52, 62, 72, and 82.
- The original notebook remains the source of truth.

Dataset files are intentionally not included in this repository.
