import gc
import numpy as np
import pandas as pd

try:
    import cudf
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

_N_ROWS = 200_000

_REGIONS = [
    "Ward-Alpha", "Ward-Beta", "Ward-Gamma", "Ward-Delta", "Ward-Epsilon",
    "ICU-North", "ICU-South", "ED-Main", "ED-Overflow", "Pediatrics",
    "Oncology", "Cardiology", "Neurology", "Orthopedics", "Maternity",
]

_RESOURCES = [
    "Ventilator", "ICU_Bed", "Surgical_Suite", "General_Bed",
    "Dialysis_Machine", "MRI_Scanner", "CT_Scanner", "Infusion_Pump",
]


def _generate_dataset():
    rng = np.random.default_rng(seed=42)

    region_arr = rng.choice(_REGIONS, size=_N_ROWS)
    severity_arr = (rng.beta(a=2, b=5, size=_N_ROWS) * 10).astype(np.float32)
    resource_arr = rng.choice(_RESOURCES, size=_N_ROWS)
    occupancy_arr = rng.uniform(0.3, 1.0, size=_N_ROWS).astype(np.float32)
    wait_time_arr = rng.exponential(scale=45, size=_N_ROWS).astype(np.float32)
    staff_ratio_arr = rng.uniform(0.1, 1.0, size=_N_ROWS).astype(np.float32)

    df_data = {
        "region": region_arr,
        "symptom_severity": severity_arr,
        "resource_required": resource_arr,
        "bed_occupancy_rate": occupancy_arr,
        "avg_wait_minutes": wait_time_arr,
        "staff_to_patient_ratio": staff_ratio_arr,
    }

    if GPU_AVAILABLE:
        return cudf.DataFrame(df_data)
    return pd.DataFrame(df_data)


def _compute_scores(df) -> list[dict]:
    if GPU_AVAILABLE:
        agg = df.groupby("region").agg(
            avg_severity=("symptom_severity", "mean"),
            avg_occupancy=("bed_occupancy_rate", "mean"),
            avg_wait=("avg_wait_minutes", "mean"),
            avg_staff_ratio=("staff_to_patient_ratio", "mean"),
            total_admissions=("symptom_severity", "count"),
        ).reset_index()
        result = agg.to_pandas()
    else:
        result = df.groupby("region").agg(
            avg_severity=("symptom_severity", "mean"),
            avg_occupancy=("bed_occupancy_rate", "mean"),
            avg_wait=("avg_wait_minutes", "mean"),
            avg_staff_ratio=("staff_to_patient_ratio", "mean"),
            total_admissions=("symptom_severity", "count"),
        ).reset_index()

    result["bottleneck_risk_score"] = (
        (result["avg_severity"] / 10.0) * 30
        + result["avg_occupancy"] * 35
        + (result["avg_wait"] / 120.0).clip(upper=1.0) * 20
        + (1 - result["avg_staff_ratio"]) * 15
    ).clip(lower=0, upper=100).round(2)

    result["status"] = result["bottleneck_risk_score"].apply(
        lambda s: "CRITICAL" if s >= 75 else ("HIGH" if s >= 55 else ("MODERATE" if s >= 35 else "LOW"))
    )

    result["avg_severity"] = result["avg_severity"].round(3)
    result["avg_occupancy"] = (result["avg_occupancy"] * 100).round(1)
    result["avg_wait"] = result["avg_wait"].round(1)
    result["avg_staff_ratio"] = result["avg_staff_ratio"].round(3)

    result = result.sort_values("bottleneck_risk_score", ascending=False)

    return result[[
        "region", "bottleneck_risk_score", "status",
        "avg_severity", "avg_occupancy", "avg_wait",
        "avg_staff_ratio", "total_admissions",
    ]].to_dict(orient="records")


def _build_cache() -> list[dict]:
    df = _generate_dataset()
    scores = _compute_scores(df)
    del df
    gc.collect()
    return scores


_cached_scores: list[dict] = _build_cache()


def get_risk_scores() -> list[dict]:
    return _cached_scores
