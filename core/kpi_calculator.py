import pandas as pd

def calculate_kpis(df):
    df = df.copy()

    # لیست ستون‌های عددی
    numeric_cols = ["Price", "Cost", "Sales 2024", "Inventory", "Annual Target", "Order"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # محاسبات پایه
    df["Gross Profit"] = (df["Price"] - df["Cost"]) * df["Sales 2024"]
    df["Inventory Value"] = df["Inventory"] * df["Cost"]
    df["Target Achievement %"] = df["Sales 2024"] / df["Annual Target"]
    df["Target Achievement %"] = df["Target Achievement %"].replace([float("inf"), -float("inf")], 0).fillna(0)
    df["Avg Monthly Sales"] = df["Sales 2024"] / 12
    df["Avg Monthly Sales"] = df["Avg Monthly Sales"].replace([float("inf"), -float("inf")], 0).fillna(0)

    # KPIهای کل
    total_sales = df["Sales 2024"].sum()
    total_revenue = (df["Sales 2024"] * df["Price"]).sum()
    gross_profit = df["Gross Profit"].sum()
    inventory_value = df["Inventory Value"].sum()

    # گروه‌بندی برای نمودار
    sales_by_model = df.groupby("Model")["Sales 2024"].sum().sort_values(ascending=False)
    orders_by_model = df.groupby("Model")["Order"].sum().sort_values(ascending=False)
    sales_by_category = df.groupby("Category")["Sales 2024"].sum().sort_values(ascending=False)

    # پرفروش‌ترین و کم‌فروش‌ترین محصول (بر اساس فروش)
    top_seller = df.loc[df["Sales 2024"].idxmax()]
    worst_seller = df.loc[df["Sales 2024"].idxmin()]

    # پرسودترین و کم‌سودترین محصول
    top_profit = df.loc[df["Gross Profit"].idxmax()]
    worst_profit = df.loc[df["Gross Profit"].idxmin()]

    # ۵ محصول پرفروش از نظر سود
    top_profitable = df.sort_values("Gross Profit", ascending=False).head(5)

    # ۵ محصول با موجودی پایین و فروش بالا
    low_stock = (df["Sales 2024"] > 0) & (df["Inventory"] < df["Avg Monthly Sales"])
    top_lowstock_highsales = df[low_stock].sort_values("Sales 2024", ascending=False).head(5)

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue,
        "gross_profit": gross_profit,
        "inventory_value": inventory_value,
        "sales_by_model": sales_by_model,
        "orders_by_model": orders_by_model,
        "sales_by_category": sales_by_category,
        "top_seller": top_seller,
        "worst_seller": worst_seller,
        "top_profit": top_profit,
        "worst_profit": worst_profit,
        "top_profitable": top_profitable,
        "top_lowstock_highsales": top_lowstock_highsales,
        "df_kpis_ready": df  # در صورت نیاز به فیلتر تعاملی در UI
    }
