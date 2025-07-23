import plotly.express as px
import pandas as pd

def plot_sales_by_model(df):
    grouped = df.groupby("Model")["Sales 2024"].sum().sort_values(ascending=False)
    return px.bar(grouped, x=grouped.index, y=grouped.values,
                  title="Sales by Model", labels={"x": "Model", "y": "Sales"})

def plot_sales_by_category(df):
    grouped = df.groupby("Category")["Sales 2024"].sum().sort_values(ascending=False)
    return px.bar(grouped, x=grouped.index, y=grouped.values,
                  title="Sales by Category", labels={"x": "Category", "y": "Sales"})

def plot_inventory_vs_sales(df):
    df_plot = df[["Model", "Inventory", "Sales 2024"]].copy()
    df_plot = df_plot.groupby("Model")[["Inventory", "Sales 2024"]].sum().reset_index()
    return px.bar(df_plot, x="Model", y=["Inventory", "Sales 2024"],
                  title="Inventory vs Sales per Model",
                  barmode="group", labels={"value": "Quantity", "variable": "Metric"})

def plot_top_profit(df):
    df_top = df.sort_values("Gross Profit", ascending=False).head(5)
    return px.bar(df_top, x="Model", y="Gross Profit", color="Category",
                  title="Top 5 Profitable Products")

def plot_risk_level_distribution(risk_counts):
    df_risk = pd.DataFrame({
        "Risk Level": list(risk_counts.keys()),
        "Count": list(risk_counts.values())
    })
    return px.pie(df_risk, values="Count", names="Risk Level", hole=0.4,
                  title="Inventory Risk Distribution")

def plot_stock_turnover(df):
    df_turnover = df[["Model", "Stock Turnover"]].copy()
    df_turnover = df_turnover.sort_values("Stock Turnover", ascending=False).head(10)
    return px.bar(df_turnover, x="Model", y="Stock Turnover",
                  title="Top 10 Stock Turnover Rates")
