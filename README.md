# CICIDS2017 Reliability Evaluation Framework

This project is an agent-friendly extraction of `CICIDS2017_Reliability_Framework_Final_Optimized_v6_FIXED.ipynb`. The experiment order and code logic are intentionally preserved.

## Research protocol
- Dataset: CICIDS2017
- Models: Logistic Regression, Random Forest, XGBoost
- Tasks: binary and multiclass classification
- Conditions: Reference, Temporal, Reference + 10% Missingness, Reference + 20% Missingness, Temporal + 10% Missingness, Temporal + 20% Missingness
- Reliability analysis: degradation, FPR, attack-level recall, temporal × missingness interaction
- Paper-mode seeds: 42, 52, 62, 72, 82
- Paper mode uses complete verified training partitions; quick validation uses bounded training subsets
- Outputs: metrics, attack-level tables, interaction tables, figures, validation and experiment metadata

## Run
The notebook remains available under `notebooks/`. For the extracted project:

```bash
python run_experiments.py
```

The original notebook was designed for Google Colab and downloads CICIDS2017 automatically. The extracted code therefore retains its original environment assumptions.

## Important execution modes
The source notebook defaults to `QUICK_VALIDATION = True` and `PAPER_MODE = False` for fast validation. Before generating final paper numbers, follow the notebook's own run instructions and complete `PAPER_MODE = True`. Do not write numerical claims into the paper before that run completes.

## Temporal validity
The final notebook explicitly prevents using `Flow Duration`, `Total TCP Flow Time`, or another model feature as a fake timestamp. If a trustworthy row-level `Timestamp` is unavailable, it uses documented CICIDS2017 capture-day/file-order provenance instead.

## Known scientific boundary
This framework evaluates the specified CICIDS2017 conditions. It does not by itself establish universal model superiority, production reliability, concept drift, adversarial robustness, or cross-dataset generalization.

## Agent instructions
Read `AGENTS.md` before modifying the experiment. Preserve the experimental protocol, avoid fabricated results, and keep paper claims tied to exported results.
