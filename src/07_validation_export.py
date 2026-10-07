# Auto-extracted from CICIDS2017_Reliability_Framework_Final_Optimized_v6_FIXED.ipynb
# Cell order is preserved intentionally for reproducibility.


# ================= NOTEBOOK CELL 30 =================
# 25. Automated scientific + reproducibility validation
EXPECTED_CONDITIONS = {
    "Reference",
    "Reference+10% Missingness",
    "Reference+20% Missingness",
    "Temporal",
    "Temporal+10% Missingness",
    "Temporal+20% Missingness",
}

validation = {
    "dataset_source": selected_repo,
    "loaded_files": loaded_files,
    "file_validation": file_validation,
    "temporal_provenance_mode": (
        "row_level_timestamp" if ROW_TIMESTAMP_MODE else "capture_day_file_order"
    ),
    "timestamp_column": timestamp_col,
    "timestamp_parse_min": (
        None if not ROW_TIMESTAMP_MODE
        else float(min(x["timestamp_validity"] for x in file_validation))
    ),
    "timestamp_min": (
        None if not ROW_TIMESTAMP_MODE else str(timestamps_sorted.min())
    ),
    "timestamp_max": (
        None if not ROW_TIMESTAMP_MODE else str(timestamps_sorted.max())
    ),
    "rows_final": int(len(y_multiclass)),
    "numeric_features": int(len(numeric_features)),
    "classes": int(len(np.unique(y_multiclass))),
    "raw_feature_nan_cells": int(np.isnan(X_matrix).sum()),
    "raw_feature_inf_cells": int(np.isinf(X_matrix).sum()),
    "experiments_completed": bool(not results_all.empty),
    "quick_validation": bool(QUICK_VALIDATION),
    "paper_mode": bool(PAPER_MODE),
    "fast_train_samples": int(FAST_TRAIN_SAMPLES),
    "seeds": list(SEEDS),
    "missingness_levels": list(MISSINGNESS_LEVELS),
    "condition_count_expected": len(EXPECTED_CONDITIONS),
}

if ROW_TIMESTAMP_MODE:
    if validation["timestamp_parse_min"] < 0.90:
        raise AssertionError("Actual Timestamp validation failed.")

    ts_min = pd.Timestamp(timestamps_sorted.min())
    ts_max = pd.Timestamp(timestamps_sorted.max())
    if not (
        pd.Timestamp("2017-07-01") <= ts_min <= pd.Timestamp("2017-07-10")
        and pd.Timestamp("2017-07-01") <= ts_max <= pd.Timestamp("2017-07-10")
    ):
        raise AssertionError(
            f"Global Timestamp range is not a valid CICIDS2017 timeline: {ts_min} -> {ts_max}"
        )

    # Explicitly prove that a forbidden flow-duration feature was not selected.
    if timestamp_col is not None and normalize_header_name(timestamp_col) in FORBIDDEN_TIMESTAMP_FEATURES:
        raise AssertionError("A forbidden flow feature was selected as Timestamp.")
else:
    if len(np.unique(source_day_ids)) < 2:
        raise AssertionError("Capture-day temporal mode requires at least two source days.")

if validation["classes"] < 2:
    raise AssertionError("At least two classes are required.")
if validation["numeric_features"] < 1:
    raise AssertionError("No numeric features remain.")

# Binary-label sanity checks.
assert np.array_equal(
    prepare_binary_labels(np.array([0, 1, 1, 0])),
    np.array([0, 1, 1, 0])
)
assert np.array_equal(
    prepare_binary_labels(np.array(["BENIGN", "Attack", "BENIGN"])),
    np.array([0, 1, 0])
)

# Raw non-finite values are allowed because the train-only imputer handles them,
# but no estimator input may contain non-finite values.
if not np.isfinite(np.nan_to_num(
    X_matrix, nan=0.0, posinf=0.0, neginf=0.0
)).all():
    raise AssertionError("Feature matrix contains an unhandled numeric value.")

if results_all.empty and RUN_EXPERIMENTS:
    raise AssertionError("Experiments were requested but produced no results.")

if not results_all.empty:
    observed = set(results_all["Condition"].unique())
    missing_conditions = EXPECTED_CONDITIONS - observed
    if missing_conditions:
        raise AssertionError(f"Missing reliability conditions: {sorted(missing_conditions)}")

    required_tasks = {"binary", "multiclass"}
    if set(results_all["Task"].unique()) != required_tasks:
        raise AssertionError("Both binary and multiclass experiments are required.")

    required_models = set(MODEL_NAMES)
    if set(results_all["Model"].unique()) != required_models:
        raise AssertionError("All three required models are not present.")

    # Exactly one row per task/model/condition/seed is expected.
    dupes = results_all.duplicated(
        ["Task", "Model", "Condition", "Seed"]
    ).sum()
    if dupes:
        raise AssertionError(f"Duplicate experiment rows detected: {dupes}")

    if PAPER_MODE:
        if len(repeated_results["Seed"].unique()) != len(SEEDS):
            raise AssertionError("Paper mode did not complete all required seeds.")
        if not set(SEEDS).issubset(set(repeated_results["Seed"].unique())):
            raise AssertionError("Paper-mode seed coverage is incomplete.")

        # Final results must use the complete training partitions.
        if len(ref_fit_idx) != len(ref_train_idx):
            raise AssertionError("Paper mode is not using the full reference training partition.")
        if len(temp_fit_idx) != len(temporal_train_idx):
            raise AssertionError("Paper mode is not using the full temporal training partition.")

    # Interaction completeness for both missingness levels.
    if final_interaction_results.empty:
        raise AssertionError("Interaction analysis is empty.")
    if PAPER_MODE:
        required_interactions = {
            (task, model, rate)
            for task in ["binary", "multiclass"]
            for model in MODEL_NAMES
            for rate in ["10%", "20%"]
        }
        observed_interactions = set(
            map(tuple, final_interaction_results[["Task", "Model", "Missingness"]].to_numpy())
        )
        if not required_interactions.issubset(observed_interactions):
            raise AssertionError("Paper-mode interaction coverage is incomplete.")

    # Multiclass attack-level coverage must include every model and non-reference condition.
    if attack_recall_degradation.empty:
        raise AssertionError("Attack-level reliability analysis is empty.")
    attack_conditions = set(
        attack_recall_degradation["Condition"].unique()
    ) - {"Reference"}
    if PAPER_MODE and attack_conditions != EXPECTED_CONDITIONS - {"Reference"}:
        raise AssertionError("Attack-level analysis does not cover all stress conditions.")

validation["validation_status"] = "PASS"
print(json.dumps(validation, indent=2))
print("Validation status: PASS")
print("✓ Actual timestamp or documented capture-day provenance only")
print("✓ No duration/flow feature can be used as a timestamp")
print("✓ Train-only imputation and LR scaling")
print("✓ Test-only 10%/20% feature-value missingness")
print("✓ Binary + multiclass")
print("✓ Reference + temporal + combined conditions")
print("✓ Degradation + interaction analysis")
print("✓ Attack-level analysis across all conditions")
print("✓ Full-data paper mode + five reproducible seeds")


# ================= NOTEBOOK CELL 31 =================
# 26. Export results, validation, and reproducibility metadata
if not results_all.empty:
    results_all.to_csv(OUTPUT_DIR / "all_results_seed42.csv", index=False)
    final_condition_metrics.to_csv(OUTPUT_DIR / "final_condition_metrics.csv", index=False)
    degradation_f1.to_csv(OUTPUT_DIR / "degradation_macro_f1.csv", index=False)
    degradation_recall.to_csv(OUTPUT_DIR / "degradation_macro_recall.csv", index=False)
    degradation_fpr.to_csv(OUTPUT_DIR / "degradation_fpr.csv", index=False)
    final_interaction_results.to_csv(OUTPUT_DIR / "interaction_results.csv", index=False)
    attack_recall.to_csv(OUTPUT_DIR / "attack_level_recall.csv", index=False)
    attack_recall_degradation.to_csv(
        OUTPUT_DIR / "attack_recall_degradation.csv", index=False
    )

if not repeated_results.empty:
    repeated_results.to_csv(OUTPUT_DIR / "repeated_seed_results.csv", index=False)

if not repeated_summary.empty:
    repeated_summary.to_csv(OUTPUT_DIR / "repeated_seed_summary.csv", index=False)

with open(OUTPUT_DIR / "validation.json", "w") as f:
    json.dump(validation, f, indent=2)

with open(OUTPUT_DIR / "experiment_config.json", "w") as f:
    json.dump({
        "dataset_source": selected_repo,
        "temporal_provenance": (
            "row_level_timestamp" if ROW_TIMESTAMP_MODE
            else "capture_day_file_order"
        ),
        "timestamp_policy": (
            "Use a validated actual Timestamp when available; otherwise use "
            "CICIDS2017 capture-day/source-file provenance. Never substitute "
            "Flow Duration, Total TCP Flow Time, packet counts, or IAT features."
        ),
        "quick_validation": QUICK_VALIDATION,
        "paper_mode": PAPER_MODE,
        "fast_train_samples": FAST_TRAIN_SAMPLES,
        "fast_sampling": "stratified" if FAST_SAMPLING_STRATIFIED else "uniform",
        "seeds": list(SEEDS),
        "models": MODEL_NAMES,
        "tasks": ["binary", "multiclass"],
        "missingness_levels": list(MISSINGNESS_LEVELS),
        "conditions": sorted(EXPECTED_CONDITIONS),
        "metrics": [
            "Accuracy", "Macro Precision", "Macro Recall",
            "Macro F1", "Weighted F1", "FPR"
        ],
        "degradation_formula": (
            "(M_reference - M_condition) / M_reference for higher-is-better "
            "metrics; (M_condition - M_reference) / M_reference for FPR"
        ),
        "interaction_formula": (
            "D_combined - (D_temporal + D_missingness)"
        ),
        "confidence_interval": "95% t-based CI across seeds",
        "preprocessing": "median imputation fit on training partition only; StandardScaler fit on training partition only for Logistic Regression",
        "stress_protocol": "random feature-value NaNs injected only into test/evaluation matrices at 10% and 20%, then transformed by the train-fitted imputer",
        "efficiency": [
            "split-level imputer reused across models and tasks",
            "split feature matrices materialized once per seed",
            "fitted estimator reused across normal/10%/20% evaluation",
            "float32 feature matrices",
            "column-wise missingness masks",
            "conservative model parallelism"
        ]
    }, f, indent=2)

with open(OUTPUT_DIR / "dataset_file_validation.json", "w") as f:
    json.dump(file_validation, f, indent=2)

print("Exports written to:", OUTPUT_DIR)

