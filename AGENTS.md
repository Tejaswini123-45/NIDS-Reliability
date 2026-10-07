# Agent Instructions — NIDS Reliability

## Project source of truth
The original notebook `notebooks/original_v6_FIXED.ipynb` is the source of truth. The files under `src/` are an ordered extraction and execution order matters.

## Research constraints
- Do not fabricate, infer, or hard-code experimental results.
- Do not invent or substitute timestamps.
- Preserve leakage-safe preprocessing: learned preprocessing must be fit on training data only.
- Keep binary and multiclass experiments separate.
- Preserve the defined reliability conditions and their semantics.
- Paper-mode requires all five seeds: 42, 52, 62, 72, 82.
- Do not add new research factors, datasets, models, or claims unless explicitly requested.
- Do not call temporal evaluation concept drift unless the experiment actually supports that claim.
- Treat the notebook and its validated configuration as authoritative when resolving implementation ambiguity.

## Workflow
1. Read `README.md` and this file before changing code.
2. Inspect the source notebook before changing scientific behavior.
3. Make the smallest change that solves the requested task.
4. Run validation before declaring an experiment complete.
5. Keep generated datasets and large raw CICIDS2017 files out of Git.
6. Never write paper claims from expected or hypothetical results.
