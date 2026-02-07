"""
Online Retail CLV Dashboard.
Run: streamlit run app/app.py (from project root)
Requires dashboard data: run python app/export_dashboard_data.py first.
"""
import json
from pathlib import Path

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from translations import TRANSLATIONS, get

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"

st.set_page_config(
    page_title="Online Retail CLV",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Light styling: consistent spacing and typography
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: "IBM Plex Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    div[data-testid="stMetricValue"] { font-size: 1.1rem; }
    .stCaptionContainer { margin-bottom: 0.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

PRIMARY = "#264653"
ACCENT = "#2A9D8F"
WARNING = "#E76F51"
NEUTRAL = "#6C757D"


def _fmt_currency(value, decimals=0):
    if value is None:
        return "-"
    if abs(value) >= 1e6:
        return f"£{value/1e6:.2f}M"
    return f"£{value:,.{decimals}f}"


def _fmt_pct(value, decimals=1):
    if value is None:
        return "-"
    return f"{value:.{decimals}f}%"


@alt.theme.register("clean", enable=True)
def _clean_altair_theme():
    return alt.theme.ThemeConfig(
        {
            "config": {
                "axis": {
                    "labelFont": "IBM Plex Sans",
                    "titleFont": "IBM Plex Sans",
                    "labelFontSize": 11,
                    "titleFontSize": 12,
                    "gridColor": "#E9ECEF",
                },
                "legend": {
                    "labelFont": "IBM Plex Sans",
                    "titleFont": "IBM Plex Sans",
                    "labelFontSize": 11,
                    "titleFontSize": 12,
                },
                "view": {"stroke": "transparent"},
            }
        }
    )


@st.cache_data
def load_dashboard_data():
    """Load dashboard data artifacts. Returns None if core files are missing."""
    clv_path = DATA_DIR / "clv_predictions.parquet"
    seg_path = DATA_DIR / "segment_summary.csv"
    cov_path = DATA_DIR / "coverage_stats.json"
    if not clv_path.exists() or not seg_path.exists() or not cov_path.exists():
        return None

    data = {
        "clv": pd.read_parquet(clv_path),
        "seg": pd.read_csv(seg_path),
    }
    with open(cov_path) as f:
        data["cov"] = json.load(f)

    optional_paths = {
        "monthly": DATA_DIR / "monthly_kpis.csv",
        "country": DATA_DIR / "country_revenue.csv",
        "retention": DATA_DIR / "cohort_retention_customers.csv",
        "retention_revenue": DATA_DIR / "cohort_retention_revenue.csv",
        "cohort_size": DATA_DIR / "cohort_size.csv",
        "avg_retention": DATA_DIR / "cohort_avg_retention.csv",
        "rfm_seg": DATA_DIR / "rfm_segment_summary.csv",
    }
    for key, path in optional_paths.items():
        data[key] = pd.read_csv(path) if path.exists() else None

    return data


def main():
    sidebar = st.sidebar
    lang = sidebar.selectbox(
        "Language / Dil",
        ["en", "tr"],
        format_func=lambda x: "English" if x == "en" else "Türkçe",
    )
    t = TRANSLATIONS[lang]

    data = load_dashboard_data()
    if data is None:
        st.warning(t["data_not_found"])
        st.stop()

    clv = data["clv"]
    seg = data["seg"]
    cov = data["cov"]
    monthly = data["monthly"]
    country = data["country"]
    retention = data["retention"]
    retention_revenue = data["retention_revenue"]
    cohort_size = data["cohort_size"]
    avg_retention = data["avg_retention"]
    rfm_seg = data["rfm_seg"]

    if monthly is not None:
        monthly["InvoiceStartMonth"] = pd.to_datetime(monthly["InvoiceStartMonth"])
    if country is not None:
        country["revenue_share_pct"] = country["revenue_share_pct"].astype(float)
    if avg_retention is not None:
        avg_retention = avg_retention.sort_values("CohortIndex")
    if cohort_size is not None:
        cohort_size = cohort_size.sort_values("CohortMonth")

    total_customers = cov.get("total_customers", clv["customer_id"].nunique())
    repeat_customers = cov.get("repeat_customers", len(clv))
    new_customers = cov.get("new_customers")
    top_1pct_share = cov.get("top_1pct_share_of_total_clv")
    total_clv = clv["clv_1y_revenue"].sum()
    total_revenue = cov.get("total_revenue")
    total_orders = cov.get("total_orders")
    date_start = cov.get("date_start")
    date_end = cov.get("date_end")

    sidebar.title(t["app_title"])
    if date_start and date_end:
        sidebar.caption(get(lang, "data_period_sidebar", start=date_start, end=date_end))
    sidebar.markdown("---")
    page_keys = ["overview", "performance", "retention", "segments", "customers", "clv_distribution", "about"]
    page = sidebar.radio(
        "Page",
        page_keys,
        format_func=lambda x: t["page_" + x],
        label_visibility="collapsed",
    )
    sidebar.markdown("---")

    if page == "overview":
        st.header(t["overview_header"])
        st.caption(t["overview_intro"])
        if date_start and date_end:
            st.caption(get(lang, "data_period", start=date_start, end=date_end))

        with st.expander(t["what_is_clv_title"]):
            st.markdown(t["what_is_clv"])

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.metric(t["total_customers"], f"{total_customers:,}")
            st.caption(t["total_customers_hint"])
        with c2:
            st.metric(t["with_clv_repeat"], f"{repeat_customers:,}")
            st.caption(t["with_clv_repeat_hint"])
        with c3:
            st.metric(t["new_single_purchase"], f"{new_customers:,}" if new_customers is not None else "-")
            st.caption(t["new_single_purchase_hint"])
        with c4:
            pct = top_1pct_share * 100 if top_1pct_share is not None else None
            st.metric(t["top_1pct_share_clv"], _fmt_pct(pct))
            st.caption(t["top_1pct_share_clv_hint"])
        with c5:
            st.metric(t["total_predicted_1y_revenue"], _fmt_currency(total_clv))
            st.caption(t["total_predicted_1y_revenue_hint"])

        share_repeat = repeat_customers / total_customers * 100 if total_customers else None
        with st.expander(t["coverage_concentration_title"]):
            if share_repeat is not None:
                st.markdown("- " + get(lang, "coverage_text", share_repeat=share_repeat))
            if top_1pct_share is not None:
                st.markdown(
                    "- "
                    + get(
                        lang,
                        "concentration_text",
                        n=cov.get("top_1pct_customers", 0),
                        pct=top_1pct_share * 100,
                    )
                )

        st.subheader(t["insights_header"])
        insights = []
        if share_repeat is not None:
            insights.append(get(lang, "insight_coverage", share=share_repeat))
        if top_1pct_share is not None:
            insights.append(get(lang, "insight_concentration", pct=top_1pct_share * 100))
        if not seg.empty:
            top_seg = seg.sort_values("total_clv", ascending=False).iloc[0]
            insights.append(
                get(
                    lang,
                    "insight_top_segment",
                    segment=top_seg["Segment"],
                    total=_fmt_currency(top_seg["total_clv"]),
                )
            )
        if avg_retention is not None and not avg_retention.empty:
            m2 = avg_retention.loc[avg_retention["CohortIndex"] == 2, "avg_retention"]
            if not m2.empty:
                insights.append(get(lang, "insight_retention_m2", m2=m2.iloc[0] * 100))
        if insights:
            st.markdown("\n".join(f"- {item}" for item in insights))

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader(t["segment_size_customers"])
            st.caption(t["segment_size_hint"])
            size_df = rfm_seg if rfm_seg is not None else seg
            size_df = size_df.sort_values("customers", ascending=False)
            ch = (
                alt.Chart(size_df)
                .mark_bar()
                .encode(
                    x=alt.X("Segment", sort="-y"),
                    y=alt.Y("customers", title=t["customers_axis_label"]),
                    color=alt.value(PRIMARY),
                    tooltip=["Segment", "customers"],
                )
                .properties(height=320)
            )
            st.altair_chart(ch, width="stretch")
        with col_b:
            st.subheader(t["total_clv_by_segment"])
            st.caption(t["total_clv_segment_hint"])
            seg_tot = seg.sort_values("total_clv", ascending=False)
            seg_tot = seg_tot.assign(total_clv_M=seg_tot["total_clv"] / 1e6)
            ch = (
                alt.Chart(seg_tot)
                .mark_bar()
                .encode(
                    x=alt.X("Segment", sort="-y"),
                    y=alt.Y("total_clv_M", title=t["total_clv_axis_label"]),
                    color=alt.value(ACCENT),
                    tooltip=["Segment", alt.Tooltip("total_clv_M", format=".2f", title="Total CLV (£M)")],
                )
                .properties(height=320)
            )
            st.altair_chart(ch, width="stretch")

    elif page == "performance":
        st.header(t["performance_header"])
        st.caption(t["performance_intro"])

        if monthly is None or country is None:
            st.info(t["performance_data_missing"])
        else:
            total_revenue = total_revenue if total_revenue is not None else monthly["revenue"].sum()
            total_orders = total_orders if total_orders is not None else int(monthly["orders"].sum())
            aov = total_revenue / total_orders if total_orders else None

            k1, k2, k3 = st.columns(3)
            with k1:
                st.metric(t["total_revenue"], _fmt_currency(total_revenue))
            with k2:
                st.metric(t["total_orders"], f"{total_orders:,}")
            with k3:
                st.metric(t["avg_order_value"], _fmt_currency(aov, decimals=0))

            m1, m2 = st.columns(2)
            with m1:
                st.subheader(t["monthly_orders"])
                ch = (
                    alt.Chart(monthly)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("InvoiceStartMonth:T", title=t["month_axis_label"]),
                        y=alt.Y("orders:Q", title=t["orders_axis_label"]),
                        color=alt.value(PRIMARY),
                        tooltip=["InvoiceStartMonth:T", "orders:Q"],
                    )
                    .properties(height=280)
                )
                st.altair_chart(ch, width="stretch")
            with m2:
                st.subheader(t["monthly_revenue"])
                ch = (
                    alt.Chart(monthly)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("InvoiceStartMonth:T", title=t["month_axis_label"]),
                        y=alt.Y("revenue:Q", title=t["revenue_axis_label"]),
                        color=alt.value(ACCENT),
                        tooltip=["InvoiceStartMonth:T", alt.Tooltip("revenue:Q", format=",.0f")],
                    )
                    .properties(height=280)
                )
                st.altair_chart(ch, width="stretch")

            st.subheader(t["monthly_aov"])
            ch = (
                alt.Chart(monthly)
                .mark_line(point=True)
                .encode(
                    x=alt.X("InvoiceStartMonth:T", title=t["month_axis_label"]),
                    y=alt.Y("aov:Q", title=t["aov_axis_label"]),
                    color=alt.value(WARNING),
                    tooltip=["InvoiceStartMonth:T", alt.Tooltip("aov:Q", format=",.0f")],
                )
                .properties(height=260)
            )
            st.altair_chart(ch, width="stretch")

            st.subheader(t["country_revenue_title"])
            filt_col1, filt_col2 = st.columns([2, 2])
            with filt_col1:
                exclude_uk = st.checkbox(t["exclude_uk"], value=True)
            with filt_col2:
                top_n = st.slider(t["top_n_countries"], min_value=5, max_value=20, value=10, step=1)

            country_plot = country.copy()
            if exclude_uk:
                country_plot = country_plot[country_plot["Country"] != "United Kingdom"]
            country_plot = country_plot.head(top_n)
            ch = (
                alt.Chart(country_plot)
                .mark_bar()
                .encode(
                    x=alt.X("Country:N", sort="-y", title=t["country_axis_label"]),
                    y=alt.Y("revenue:Q", title=t["revenue_axis_label"]),
                    color=alt.value(PRIMARY),
                    tooltip=["Country", alt.Tooltip("revenue:Q", format=",.0f"), "orders:Q"],
                )
                .properties(height=320)
            )
            st.altair_chart(ch, width="stretch")

            with st.expander(t["country_table_expander"]):
                st.dataframe(
                    country_plot.style.format({"revenue": "{:,.0f}", "revenue_share_pct": "{:.2f}"}),
                    width="stretch",
                )

    elif page == "retention":
        st.header(t["retention_header"])
        st.caption(t["retention_intro"])

        if retention is None or retention_revenue is None or cohort_size is None or avg_retention is None:
            st.info(t["retention_data_missing"])
        else:
            cohort_order = sorted(retention["CohortMonth"].unique())
            show_values = st.checkbox(t["show_values"], value=False)
            tab_c, tab_r = st.tabs([t["customer_retention_tab"], t["revenue_retention_tab"]])
            with tab_c:
                st.subheader(t["cohort_heatmap_customers"])
                heat_base = (
                    alt.Chart(retention)
                    .mark_rect()
                    .encode(
                        x=alt.X("CohortIndex:O", title=t["cohort_index_label"]),
                        y=alt.Y("CohortMonth:O", sort=cohort_order, title=t["cohort_month_label"]),
                        color=alt.Color("retention_rate:Q", scale=alt.Scale(scheme="greens")),
                        tooltip=[
                            "CohortMonth",
                            "CohortIndex",
                            alt.Tooltip("retention_rate:Q", format=".0%"),
                        ],
                    )
                    .properties(height=380)
                )
                if show_values:
                    text = (
                        alt.Chart(retention)
                        .mark_text(size=9, color="#111111")
                        .encode(
                            x=alt.X("CohortIndex:O"),
                            y=alt.Y("CohortMonth:O", sort=cohort_order),
                            text=alt.Text("retention_rate:Q", format=".0%"),
                        )
                    )
                    st.altair_chart(heat_base + text, width="stretch")
                else:
                    st.altair_chart(heat_base, width="stretch")
            with tab_r:
                st.subheader(t["cohort_heatmap_revenue"])
                heat_base = (
                    alt.Chart(retention_revenue)
                    .mark_rect()
                    .encode(
                        x=alt.X("CohortIndex:O", title=t["cohort_index_label"]),
                        y=alt.Y("CohortMonth:O", sort=cohort_order, title=t["cohort_month_label"]),
                        color=alt.Color("retention_rate:Q", scale=alt.Scale(scheme="blues")),
                        tooltip=[
                            "CohortMonth",
                            "CohortIndex",
                            alt.Tooltip("retention_rate:Q", format=".0%"),
                        ],
                    )
                    .properties(height=380)
                )
                if show_values:
                    text = (
                        alt.Chart(retention_revenue)
                        .mark_text(size=9, color="#111111")
                        .encode(
                            x=alt.X("CohortIndex:O"),
                            y=alt.Y("CohortMonth:O", sort=cohort_order),
                            text=alt.Text("retention_rate:Q", format=".0%"),
                        )
                    )
                    st.altair_chart(heat_base + text, width="stretch")
                else:
                    st.altair_chart(heat_base, width="stretch")

            st.caption(t["retention_note"])

            r1, r2 = st.columns(2)
            with r1:
                st.subheader(t["avg_retention_curve"])
                ch = (
                    alt.Chart(avg_retention)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("CohortIndex:O", title=t["cohort_index_label"]),
                        y=alt.Y("avg_retention:Q", title=t["retention_rate_label"]),
                        color=alt.value(ACCENT),
                        tooltip=[
                            "CohortIndex",
                            alt.Tooltip("avg_retention:Q", format=".0%"),
                        ],
                    )
                    .properties(height=260)
                )
                st.altair_chart(ch, width="stretch")
            with r2:
                st.subheader(t["cohort_size_chart"])
                ch = (
                    alt.Chart(cohort_size)
                    .mark_bar()
                    .encode(
                        x=alt.X("CohortMonth:O", sort=cohort_order, title=t["cohort_month_label"]),
                        y=alt.Y("customers:Q", title=t["customers_axis_label"]),
                        color=alt.value(PRIMARY),
                        tooltip=["CohortMonth", "customers:Q"],
                    )
                    .properties(height=260)
                )
                st.altair_chart(ch, width="stretch")

    elif page == "segments":
        st.header(t["segments_header"])
        st.markdown(t["segments_intro"])
        st.caption(t["segments_caption"])

        if rfm_seg is not None:
            tab_clv, tab_rfm = st.tabs([t["tab_clv"], t["tab_rfm"]])
        else:
            tab_clv = st.container()
            tab_rfm = None

        with tab_clv:
            seg_display = seg.copy()
            seg_display["total_clv_M"] = seg_display["total_clv"] / 1e6
            st.dataframe(
                seg_display.style.format(
                    {
                        "total_clv": "{:,.0f}",
                        "mean_clv": "{:,.0f}",
                        "median_clv": "{:,.0f}",
                        "total_clv_M": "{:.2f}",
                    }
                ),
                width="stretch",
            )

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(t["total_clv_by_segment"])
                st.caption(t["total_clv_segment_hint"])
                seg_tot = seg.sort_values("total_clv", ascending=False)
                seg_tot = seg_tot.assign(total_clv_M=seg_tot["total_clv"] / 1e6)
                ch = (
                    alt.Chart(seg_tot)
                    .mark_bar()
                    .encode(
                        x=alt.X("Segment", sort="-y"),
                        y=alt.Y("total_clv_M", title=t["total_clv_axis_label"]),
                        color=alt.value(PRIMARY),
                    )
                    .properties(height=350)
                )
                st.altair_chart(ch, width="stretch")
            with col2:
                st.subheader(t["median_clv_by_segment"])
                st.caption(t["median_clv_segment_hint"])
                seg_plot = seg.sort_values("median_clv", ascending=False)
                ch = (
                    alt.Chart(seg_plot)
                    .mark_bar()
                    .encode(
                        x=alt.X("Segment", sort="-y"),
                        y=alt.Y("median_clv", title=t["median_clv_axis_label"]),
                        color=alt.value(ACCENT),
                    )
                    .properties(height=350)
                )
                st.altair_chart(ch, width="stretch")

            st.download_button(
                label=t["download_segment_summary"],
                data=seg.to_csv(index=False),
                file_name="segment_summary.csv",
                mime="text/csv",
            )

        if tab_rfm is not None:
            with tab_rfm:
                st.subheader(t["rfm_segment_summary"])
                st.caption(t["rfm_segment_hint"])
                rfm_display = rfm_seg.copy()
                st.dataframe(
                    rfm_display.style.format(
                        {
                            "revenue_total": "{:,.0f}",
                            "revenue_avg": "{:,.0f}",
                            "recency_avg": "{:,.1f}",
                            "frequency_avg": "{:,.1f}",
                            "customer_share_pct": "{:.2f}",
                            "revenue_share_pct": "{:.2f}",
                        }
                    ),
                    width="stretch",
                )
                ch = (
                    alt.Chart(rfm_display)
                    .mark_bar()
                    .encode(
                        x=alt.X("Segment", sort="-y"),
                        y=alt.Y("revenue_share_pct", title=t["revenue_share_axis_label"]),
                        color=alt.value(WARNING),
                        tooltip=["Segment", alt.Tooltip("revenue_share_pct", format=".2f")],
                    )
                    .properties(height=320)
                )
                st.altair_chart(ch, width="stretch")

    elif page == "customers":
        st.header(t["customers_header"])
        st.markdown(t["customers_intro"])

        with st.expander(t["customers_columns_expander_title"]):
            st.markdown("- **P(Alive):** " + t["column_p_alive"])
            st.markdown("- **Expected purchases (365):** " + t["column_expected_purchases"])
            st.markdown("- **CLV (1Y revenue):** " + t["column_clv_1y"])

        filt_col1, filt_col2, filt_col3 = st.columns([2, 2, 2])
        with filt_col1:
            segment_filter = st.selectbox(
                t["segment"],
                ["All"] + sorted(clv["Segment"].dropna().unique().tolist()),
            )
        with filt_col2:
            p_alive_min = st.slider(t["p_alive_min"], min_value=0.0, max_value=1.0, value=0.0, step=0.05)
        with filt_col3:
            min_clv = st.number_input(t["min_clv"], min_value=0.0, value=0.0, step=100.0)

        customer_search = st.text_input(t["customer_id_optional"], placeholder=t["customer_id_placeholder"])

        if segment_filter != "All":
            df_c = clv[clv["Segment"] == segment_filter].copy()
        else:
            df_c = clv.copy()

        df_c = df_c[df_c["p_alive"] >= p_alive_min]
        df_c = df_c[df_c["clv_1y_revenue"] >= min_clv]

        if customer_search.strip():
            try:
                cid = int(customer_search.strip())
                df_c = df_c[df_c["customer_id"] == cid]
            except ValueError:
                pass

        n_options = [10, 25, 50, 100, 200, 500]
        n = st.select_slider(t["show_top_n_by_clv"], options=n_options, value=100)
        df_c = df_c.nlargest(n, "clv_1y_revenue")

        r1, r2 = st.columns([1, 3])
        with r1:
            st.metric(t["rows_shown"], len(df_c))
        with r2:
            sum_clv = df_c["clv_1y_revenue"].sum()
            st.metric(t["sum_displayed_clv"], f"£{sum_clv:,.0f}")
            st.caption(t["sum_displayed_clv_hint"])

        display_cols = [
            "customer_id",
            "Segment",
            "frequency",
            "p_alive",
            "expected_purchases_365",
            "expected_avg_value",
            "clv_1y_revenue",
        ]
        display_df = df_c[display_cols].copy()
        st.dataframe(
            display_df.style.format(
                {
                    "p_alive": "{:.2f}",
                    "expected_purchases_365": "{:.2f}",
                    "expected_avg_value": "{:.2f}",
                    "clv_1y_revenue": "{:,.0f}",
                }
            ),
            width="stretch",
        )
        st.download_button(
            label=t["download_current_table"],
            data=display_df.to_csv(index=False),
            file_name="clv_customers.csv",
            mime="text/csv",
        )

    elif page == "clv_distribution":
        st.header(t["clv_distribution_header"])
        st.markdown(t["clv_distribution_intro"])
        st.caption(t["clv_distribution_caption"])

        seg_for_dist = st.selectbox(
            t["segment_for_distribution"],
            ["All"] + sorted(clv["Segment"].dropna().unique().tolist()),
            key="dist_seg",
        )
        if seg_for_dist != "All":
            dist_series = clv[clv["Segment"] == seg_for_dist]["clv_1y_revenue"]
        else:
            dist_series = clv["clv_1y_revenue"]

        if len(dist_series) == 0:
            st.info(t["no_data_segment"])
            st.stop()

        q98 = dist_series.quantile(0.98)
        q98 = max(q98, dist_series.median() * 0.01, 1.0)
        bins_raw = np.linspace(0, q98, 40)
        hist_raw = dist_series.clip(upper=bins_raw[-1]).value_counts(bins=bins_raw).sort_index()
        hist_df_raw = pd.DataFrame(
            {
                "bin_min": [x.left for x in hist_raw.index],
                "bin_max": [x.right for x in hist_raw.index],
                "count": hist_raw.values,
                "label": [f"{x.left:.0f}-{x.right:.0f}" for x in hist_raw.index],
            }
        )

        log_clv = np.log10(dist_series.replace(0, np.nan).dropna())
        has_log = len(log_clv) > 0
        if has_log:
            bins_log = np.linspace(log_clv.min(), log_clv.max(), 30)
            hist_log = log_clv.value_counts(bins=bins_log).sort_index()
            hist_df_log = pd.DataFrame(
                {
                    "bin_min": [x.left for x in hist_log.index],
                    "count": hist_log.values,
                    "label": [f"{x.left:.2f}-{x.right:.2f}" for x in hist_log.index],
                }
            )

        d1, d2 = st.columns(2)
        with d1:
            st.subheader(t["clv_raw_histogram"])
            ch_raw = (
                alt.Chart(hist_df_raw)
                .mark_bar()
                .encode(
                    x=alt.X("label", title=t["clv_bin_axis_label"], sort=None),
                    y=alt.Y("count", title=t["count_axis_label"]),
                    color=alt.value(PRIMARY),
                )
                .properties(height=350)
            )
            st.altair_chart(ch_raw, width="stretch")
        with d2:
            st.subheader(t["clv_log_histogram"])
            if has_log:
                ch_log = (
                    alt.Chart(hist_df_log)
                    .mark_bar()
                    .encode(
                        x=alt.X("label", title=t["clv_log_axis_label"], sort=None),
                        y=alt.Y("count", title=t["count_axis_label"]),
                        color=alt.value(ACCENT),
                    )
                    .properties(height=350)
                )
                st.altair_chart(ch_log, width="stretch")
            else:
                st.info(t["no_positive_log"])

        st.subheader(t["summary_stats_clv"])
        st.caption(t["summary_stats_hint"])
        sum_df = dist_series.agg(["count", "mean", "median", "min", "max"]).to_frame().T
        sum_df.columns = ["Count", "Mean", "Median", "Min", "Max"]
        st.dataframe(sum_df.style.format("{:,.0f}"), width="stretch")

    else:  # about
        st.header(t["about_header"])
        st.caption(t["about_intro"])
        st.markdown(t["about_body"])
        with st.expander(t["how_to_use_title"]):
            st.markdown(t["how_to_use_body"])


if __name__ == "__main__":
    main()
