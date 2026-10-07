# AGENTS.md

## Project goal
Maintain and extend a reproducible research framework for evaluating ML-based Network Intrusion Detection Systems under temporal and controlled feature-missingness conditions.

## Non-negotiable rules
1. Do not fabricate, estimate, or manually invent experimental results.
2. Do not replace the temporal provenance policy with a flow-duration or other feature-derived fake timestamp.
3. Preserve leakage-safe preprocessing: learned transformations are fitted on training data only.
4. Keep binary and multiclass experiments separate.
5. Keep LR, RF, and XGBoost as the current model set unless the user explicitly expands scope.
6. Preserve the defined missingness levels and combined temporal + missingness conditions.
7. Do not call the temporal experiment proof of concept drift.
8. Do not claim adversarial robustness, production readiness, universal model superiority, or cross-dataset generalization from this project.
9. Paper-mode results must come from the completed five-seed protocol.
10. When changing experiment logic, update the exported configuration/metadata and README if the protocol changes.

## Source of truth
`notebooks/original_v6_FIXED.ipynb` is the original source. The `src/` files are an ordered extraction of its code cells. Preserve execution order unless deliberately refactoring the shared-state design and validating that outputs remain identical.

## Current priority
Finish and validate the promised core experiments first. Do not add unrelated models, datasets, SHAP, transformers, or new stress mechanisms unless explicitly requested.
