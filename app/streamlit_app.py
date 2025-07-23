import streamlit as st
import pandas as pd
import tempfile
import sys
import os

# افزودن مسیر والد برای import بقیه فایل‌ها
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import فایل‌های داخلی
from core.data_loader import load_and_prepare_data
from core.kpi_calculator import calculate_kpis
from core.inventory_analysis import analyze_inventory
from report.chart_generator import (
    plot_sales_by_model,
    plot_sales_by_category,
    plot_inventory_vs_sales,
    plot_top_profit,
    plot_risk_level_distribution,
    plot_stock_turnover
)
from report.insight_text import generate_insight_text
from report.report_exporter import export_report

# تنظیمات صفحه
st.set_page_config(page_title="Sales & Inventory Dashboard", layout="wide")
st.title("📊 Volvo Inventory & Sales Dashboard")

# مسیر فایل داده
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'volvo_data.csv')

# بارگذاری و پاکسازی داده
df_raw = load_and_prepare_data(DATA_PATH)

# 1️⃣ فیلترهای تعاملی در سایدبار
with st.sidebar:
    st.header("🔎 Filters")
    selected_model = st.multiselect("Filter by Model", options=sorted(df_raw["Model"].unique()), default=None)
    categories = sorted([str(x) for x in df_raw["Category"].unique()])
    selected_category = st.multiselect("Filter by Category", options=categories, default=None)

df = df_raw.copy()
if selected_model:
    df = df[df["Model"].isin(selected_model)]
if selected_category:
    df = df[df["Category"].isin(selected_category)]

# 2️⃣ KPI محاسباتی و تحلیل انبار
kpis = calculate_kpis(df)
df_kpi_ready = kpis["df_kpis_ready"]
inventory = analyze_inventory(df_kpi_ready)
insight_text = generate_insight_text(kpis, inventory)

# 3️⃣ نمایش KPIها
st.header("📌 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Sales", f"{int(kpis['total_sales']):,}")
col2.metric("Revenue (£)", f"{round(kpis['total_revenue']):,}")
col3.metric("Gross Profit (£)", f"{round(kpis['gross_profit']):,}")
col4.metric("Inventory Value (£)", f"{round(kpis['inventory_value']):,}")
col5.metric("Avg Stock Turnover", inventory['average_turnover'])

st.markdown("---")

# 4️⃣ نمودارهای فروش و سود
st.subheader("📊 Sales Overview")
col6, col7 = st.columns(2)
col6.plotly_chart(plot_sales_by_model(df), use_container_width=True)
col7.plotly_chart(plot_sales_by_category(df), use_container_width=True)
st.plotly_chart(plot_top_profit(df_kpi_ready), use_container_width=True)

st.markdown("---")

# 5️⃣ نمودارهای تحلیل انبار
st.subheader("🚨 Inventory Insights")
col8, col9 = st.columns(2)
col8.plotly_chart(plot_inventory_vs_sales(df), use_container_width=True)
col9.plotly_chart(plot_risk_level_distribution(inventory["risk_counts"]), use_container_width=True)
st.plotly_chart(plot_stock_turnover(inventory["df_with_risk"]), use_container_width=True)

st.markdown("---")

# 6️⃣ جدول‌های تحلیلی ریسک انبار
st.subheader("📋 Inventory Risk Tables")
with st.expander("🟥 High-Demand Risk (Low Inventory, High Sales)"):
    st.dataframe(inventory["risky_items"], use_container_width=True)

with st.expander("🟡 Slow-Moving Items"):
    st.dataframe(inventory["slow_moving"], use_container_width=True)

with st.expander("⬛ Dead Stock (No Sales)"):
    st.dataframe(inventory["dead_stock"], use_container_width=True)

with st.expander("🟦 Out-of-Stock but In Demand"):
    st.dataframe(inventory["out_of_stock_high_demand"], use_container_width=True)

with st.expander("🕳️ Zero-Zero Products"):
    st.dataframe(inventory["zero_zero_items"], use_container_width=True)

st.markdown("---")

# 7️⃣ خلاصه تحلیلی
st.subheader("🧠 Insight Summary")
st.text(insight_text)

st.markdown("---")

# 8️⃣ خروجی PDF با نمودارها
st.subheader("📄 Export Full Report")
if st.button("Generate PDF Report"):
    with st.spinner("Building PDF..."):
        with tempfile.TemporaryDirectory() as tmpdir:
            # ذخیره نمودارها
            plot_sales_by_model(df).write_image(f"{tmpdir}/model_sales.png")
            plot_sales_by_category(df).write_image(f"{tmpdir}/category_sales.png")
            plot_inventory_vs_sales(df).write_image(f"{tmpdir}/inventory_vs_sales.png")
            plot_top_profit(df).write_image(f"{tmpdir}/top_profit.png")
            plot_risk_level_distribution(inventory["risk_counts"]).write_image(f"{tmpdir}/risk_pie.png")
            plot_stock_turnover(inventory["df_with_risk"]).write_image(f"{tmpdir}/turnover.png")

            chart_paths = [
                f"{tmpdir}/model_sales.png",
                f"{tmpdir}/category_sales.png",
                f"{tmpdir}/inventory_vs_sales.png",
                f"{tmpdir}/top_profit.png",
                f"{tmpdir}/risk_pie.png",
                f"{tmpdir}/turnover.png"
            ]

            pdf_path = f"{tmpdir}/report.pdf"
            export_report(kpis, insight_text, chart_paths, pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name="Volvo_Report.pdf",
                    mime="application/pdf"
                )
