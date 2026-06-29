import numpy as np
import pandas as pd

try:
    import cudf
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def generate_mock_dataset(n_rows: int = 1_000_000) -> "cudf.DataFrame | pd.DataFrame":
    rng = np.random.default_rng(seed=42)

    regions = ["Ward-Alpha", "Ward-Beta", "Ward-Gamma", "Ward-Delta", "Ward-Epsilon",
               "ICU-North", "ICU-South", "ED-Main", "ED-Overflow", "Pediatrics",
               "Oncology", "Cardiology", "Neurology", "Orthopedics", "Maternity"]

    resources = ["Ventilator", "ICU_Bed", "Surgical_Suite", "General_Bed",
                 "Dialysis_Machine", "MRI_Scanner", "CT_Scanner", "Infusion_Pump"]

    timestamps = pd.date_range("2024-01-01", periods=n_rows, freq="3s")
    region_arr = rng.choice(regions, size=n_rows)
    severity_arr = rng.beta(a=2, b=5, size=n_rows) * 10
    resource_arr = rng.choice(resources, size=n_rows)
    occupancy_arr = rng.uniform(0.3, 1.0, size=n_rows)
    wait_time_arr = rng.exponential(scale=45, size=n_rows)
    staff_ratio_arr = rng.uniform(0.1, 1.0, size=n_rows)

    df_data = {
        "timestamp": timestamps,
        "region": region_arr,
        "symptom_severity": severity_arr.astype(np.float32),
        "resource_required": resource_arr,
        "bed_occupancy_rate": occupancy_arr.astype(np.float32),
        "avg_wait_minutes": wait_time_arr.astype(np.float32),
        "staff_to_patient_ratio": staff_ratio_arr.astype(np.float32),
    }

    if GPU_AVAILABLE:
        return cudf.DataFrame(df_data)
    return pd.DataFrame(df_data)


def compute_bottleneck_scores(df) -> list[dict]:
    if GPU_AVAILABLE:
        agg = df.groupby("region").agg(
            avg_severity=("symptom_severity", "mean"),
            avg_occupancy=("bed_occupancy_rate", "mean"),
            avg_wait=("avg_wait_minutes", "mean"),
            avg_staff_ratio=("staff_to_patient_ratio", "mean"),
            total_admissions=("symptom_severity", "count"),
        ).reset_index()
        result_df = agg.to_pandas()
    else:
        result_df = df.groupby("region").agg(
            avg_severity=("symptom_severity", "mean"),
            avg_occupancy=("bed_occupancy_rate", "mean"),
            avg_wait=("avg_wait_minutes", "mean"),
            avg_staff_ratio=("staff_to_patient_ratio", "mean"),
            total_admissions=("symptom_severity", "count"),
        ).reset_index()

    result_df["severity_score"] = (result_df["avg_severity"] / 10.0) * 30
    result_df["occupancy_score"] = result_df["avg_occupancy"] * 35
    result_df["wait_score"] = (result_df["avg_wait"] / 120.0).clip(upper=1.0) * 20
    result_df["staff_penalty"] = (1 - result_df["avg_staff_ratio"]) * 15

    result_df["bottleneck_risk_score"] = (
        result_df["severity_score"]
        + result_df["occupancy_score"]
        + result_df["wait_score"]
        + result_df["staff_penalty"]
    ).clip(lower=0, upper=100).round(2)

    result_df["status"] = result_df["bottleneck_risk_score"].apply(
        lambda s: "CRITICAL" if s >= 75 else ("HIGH" if s >= 55 else ("MODERATE" if s >= 35 else "LOW"))
    )

    result_df["avg_severity"] = result_df["avg_severity"].round(3)
    result_df["avg_occupancy"] = (result_df["avg_occupancy"] * 100).round(1)
    result_df["avg_wait"] = result_df["avg_wait"].round(1)
    result_df["avg_staff_ratio"] = result_df["avg_staff_ratio"].round(3)

    result_df = result_df.sort_values("bottleneck_risk_score", ascending=False)

    records = result_df[[
        "region", "bottleneck_risk_score", "status",
        "avg_severity", "avg_occupancy", "avg_wait",
        "avg_staff_ratio", "total_admissions"
    ]].to_dict(orient="records")

    return records


_cached_scores: list[dict] | None = None


def get_risk_scores() -> list[dict]:
    global _cached_scores
    if _cached_scores is None:
        df = generate_mock_dataset(1_000_000)
        _cached_scores = compute_bottleneck_scores(df)
    return _cached_scores
