"""
Export dashboard data from the CLV pipeline.
Run once after notebook 01 (to have online_retail_clean.parquet and rfm_segments.csv).
Writes CLV, EDA, and retention artifacts to data/ for the Streamlit dashboard.
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data

warnings.filterwarnings("ignore")

# Paths: run from project root or app/
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

def main():
    data_dir = DATA_DIR
    if not (data_dir / "online_retail_clean.parquet").exists():
        raise FileNotFoundError(
            "data/online_retail_clean.parquet not found. Run notebook 01_eda_rfm.ipynb first."
        )
    if not (data_dir / "rfm_segments.csv").exists():
        raise FileNotFoundError(
            "data/rfm_segments.csv not found. Run notebook 01_eda_rfm.ipynb first."
        )

    df = pd.read_parquet(data_dir / "online_retail_clean.parquet")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceStartMonth"] = df["InvoiceDate"].values.astype("datetime64[M]")
    analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    summary = summary_data_from_transaction_data(
        df,
        customer_id_col="Customer ID",
        datetime_col="InvoiceDate",
        monetary_value_col="TotalPrice",
        observation_period_end=analysis_date,
    )

    # BG/NBD
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(summary["frequency"], summary["recency"], summary["T"])
    summary["p_alive"] = bgf.conditional_probability_alive(
        summary["frequency"], summary["recency"], summary["T"]
    )
    summary["expected_purchases_365"] = bgf.conditional_expected_number_of_purchases_up_to_time(
        365, summary["frequency"], summary["recency"], summary["T"]
    )

    # Gamma-Gamma (repeat only)
    summary_with_value = summary[summary["frequency"] > 0].copy()
    ggf = GammaGammaFitter(penalizer_coef=0.001)
    ggf.fit(summary_with_value["frequency"], summary_with_value["monetary_value"])
    summary_with_value["expected_avg_value"] = ggf.conditional_expected_average_profit(
        summary_with_value["frequency"], summary_with_value["monetary_value"]
    )

    clv_df = summary_with_value.copy()
    clv_df["clv_1y_revenue"] = (
        clv_df["expected_purchases_365"] * clv_df["expected_avg_value"]
    )

    rfm = pd.read_csv(data_dir / "rfm_segments.csv")
    rfm = rfm.rename(columns={"Customer ID": "customer_id"})
    clv_segmented = (
        clv_df.reset_index()
        .rename(columns={"Customer ID": "customer_id"})
        .merge(
            rfm[["customer_id", "Segment", "is_vip", "is_b2b"]],
            on="customer_id",
            how="left",
        )
    )

    segment_value = (
        clv_segmented.groupby("Segment")["clv_1y_revenue"]
        .agg(
            customers="count",
            total_clv="sum",
            mean_clv="mean",
            median_clv="median",
        )
        .sort_values("total_clv", ascending=False)
    )

    total_customers = len(summary)
    repeat_customers = (summary["frequency"] > 0).sum()
    new_customers = (summary["frequency"] == 0).sum()
    clv_sorted = clv_segmented.sort_values("clv_1y_revenue", ascending=False)
    top_1pct_n = max(1, int(np.ceil(0.01 * len(clv_sorted))))
    top_1pct_share = (
        clv_sorted.head(top_1pct_n)["clv_1y_revenue"].sum()
        / clv_sorted["clv_1y_revenue"].sum()
    )

    # ---- EDA aggregates (from notebooks) ----
    monthly = (
        df.groupby("InvoiceStartMonth")
        .agg(
            orders=("Invoice", "nunique"),
            revenue=("TotalPrice", "sum"),
        )
        .reset_index()
        .sort_values("InvoiceStartMonth")
    )
    monthly["aov"] = monthly["revenue"] / monthly["orders"]

    country = (
        df.groupby("Country")
        .agg(
            orders=("Invoice", "nunique"),
            revenue=("TotalPrice", "sum"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    total_revenue = float(country["revenue"].sum())
    country["revenue_share_pct"] = country["revenue"] / total_revenue * 100

    # ---- Cohort retention (customers & revenue) ----
    tx = df[["Customer ID", "InvoiceStartMonth", "TotalPrice"]].copy()
    cohort = (
        tx.groupby("Customer ID")["InvoiceStartMonth"]
        .min()
        .reset_index()
        .rename(columns={"InvoiceStartMonth": "CohortMonth"})
    )
    tx = tx.merge(cohort, on="Customer ID", how="left")
    tx["CohortIndex"] = (
        (tx["InvoiceStartMonth"].dt.year - tx["CohortMonth"].dt.year) * 12
        + (tx["InvoiceStartMonth"].dt.month - tx["CohortMonth"].dt.month)
        + 1
    )

    cohort_counts = (
        tx.groupby(["CohortMonth", "CohortIndex"])["Customer ID"]
        .nunique()
        .reset_index()
        .pivot(index="CohortMonth", columns="CohortIndex", values="Customer ID")
        .sort_index()
    )
    retention = cohort_counts.divide(cohort_counts.iloc[:, 0], axis=0)

    rev = (
        tx.groupby(["CohortMonth", "CohortIndex"])["TotalPrice"]
        .sum()
        .reset_index()
        .pivot(index="CohortMonth", columns="CohortIndex", values="TotalPrice")
        .sort_index()
    )
    rev_retention = rev.divide(rev.iloc[:, 0], axis=0)

    retention_long = (
        retention.reset_index()
        .melt(id_vars="CohortMonth", var_name="CohortIndex", value_name="retention_rate")
        .dropna()
    )
    retention_long["CohortMonth"] = retention_long["CohortMonth"].dt.strftime("%Y-%m")
    retention_long["CohortIndex"] = retention_long["CohortIndex"].astype(int)

    rev_retention_long = (
        rev_retention.reset_index()
        .melt(id_vars="CohortMonth", var_name="CohortIndex", value_name="retention_rate")
        .dropna()
    )
    rev_retention_long["CohortMonth"] = rev_retention_long["CohortMonth"].dt.strftime("%Y-%m")
    rev_retention_long["CohortIndex"] = rev_retention_long["CohortIndex"].astype(int)

    cohort_size = cohort_counts.iloc[:, 0].reset_index()
    cohort_size.columns = ["CohortMonth", "customers"]
    cohort_size["CohortMonth"] = cohort_size["CohortMonth"].dt.strftime("%Y-%m")

    avg_retention = retention.mean(axis=0).reset_index()
    avg_retention.columns = ["CohortIndex", "avg_retention"]
    avg_retention["CohortIndex"] = avg_retention["CohortIndex"].astype(int)

    # RFM segment summary (non-CLV) for context
    seg_rfm = (
        rfm.groupby("Segment")
        .agg(
            customers=("customer_id", "size"),
            revenue_total=("Monetary", "sum"),
            revenue_avg=("Monetary", "mean"),
            recency_avg=("Recency", "mean"),
            frequency_avg=("Frequency", "mean"),
        )
        .reset_index()
    )
    seg_rfm["customer_share_pct"] = seg_rfm["customers"] / seg_rfm["customers"].sum() * 100
    seg_rfm["revenue_share_pct"] = seg_rfm["revenue_total"] / seg_rfm["revenue_total"].sum() * 100
    seg_rfm = seg_rfm.sort_values("revenue_total", ascending=False)

    # Save
    out_cols = [
        "customer_id",
        "Segment",
        "is_vip",
        "is_b2b",
        "frequency",
        "p_alive",
        "expected_purchases_365",
        "expected_avg_value",
        "clv_1y_revenue",
    ]
    clv_segmented[out_cols].to_parquet(
        data_dir / "clv_predictions.parquet", index=False
    )
    segment_value.reset_index().to_csv(
        data_dir / "segment_summary.csv", index=False
    )
    monthly.to_csv(data_dir / "monthly_kpis.csv", index=False)
    country.to_csv(data_dir / "country_revenue.csv", index=False)
    retention_long.to_csv(data_dir / "cohort_retention_customers.csv", index=False)
    rev_retention_long.to_csv(data_dir / "cohort_retention_revenue.csv", index=False)
    cohort_size.to_csv(data_dir / "cohort_size.csv", index=False)
    avg_retention.to_csv(data_dir / "cohort_avg_retention.csv", index=False)
    seg_rfm.to_csv(data_dir / "rfm_segment_summary.csv", index=False)
    with open(data_dir / "coverage_stats.json", "w") as f:
        json.dump(
            {
                "total_customers": int(total_customers),
                "repeat_customers": int(repeat_customers),
                "new_customers": int(new_customers),
                "top_1pct_customers": int(top_1pct_n),
                "top_1pct_share_of_total_clv": float(top_1pct_share),
                "total_revenue": float(df["TotalPrice"].sum()),
                "total_orders": int(df["Invoice"].nunique()),
                "date_start": df["InvoiceDate"].min().date().isoformat(),
                "date_end": df["InvoiceDate"].max().date().isoformat(),
            },
            f,
            indent=2,
        )

    print("Dashboard data exported to data/:")
    print("  - clv_predictions.parquet")
    print("  - segment_summary.csv")
    print("  - rfm_segment_summary.csv")
    print("  - monthly_kpis.csv")
    print("  - country_revenue.csv")
    print("  - cohort_retention_customers.csv")
    print("  - cohort_retention_revenue.csv")
    print("  - cohort_size.csv")
    print("  - cohort_avg_retention.csv")
    print("  - coverage_stats.json")


if __name__ == "__main__":
    main()
