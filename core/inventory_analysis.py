import pandas as pd

def analyze_inventory(df):
    """
    Perform inventory-level analysis including risk level, turnover, dead stock,
    slow-moving items, and high-demand low-stock detection.

    Args:
        df (pd.DataFrame): Cleaned DataFrame with Avg Monthly Sales calculated.

    Returns:
        dict: Inventory insights and filtered product subsets.
    """
    df = df.copy()

    # اطمینان از عددی بودن
    df["Inventory"] = pd.to_numeric(df["Inventory"], errors="coerce").fillna(0)
    df["Sales 2024"] = pd.to_numeric(df["Sales 2024"], errors="coerce").fillna(0)
    df["Avg Monthly Sales"] = pd.to_numeric(df["Avg Monthly Sales"], errors="coerce").fillna(0)

    # --- نسبت موجودی به فروش ماهانه ---
    df["Inventory/Sales Ratio"] = df["Inventory"] / df["Avg Monthly Sales"]
    df["Inventory/Sales Ratio"] = df["Inventory/Sales Ratio"].replace([float("inf"), -float("inf")], 0).fillna(0)

    def classify_risk(ratio):
        if ratio < 1:
            return "High Risk"
        elif ratio <= 3:
            return "Medium Risk"
        else:
            return "Overstock"
    df["Inventory Risk Level"] = df["Inventory/Sales Ratio"].apply(classify_risk)
    risk_counts = df["Inventory Risk Level"].value_counts().to_dict()

    # --- Stock Turnover Ratio ---
    # فرمول = Sales / Average Inventory (اینجا موجودی فعلی فرض شده)
    df["Stock Turnover"] = df["Sales 2024"] / df["Inventory"]
    df["Stock Turnover"] = df["Stock Turnover"].replace([float("inf"), -float("inf")], 0).fillna(0)
    average_turnover = round(df["Stock Turnover"].mean(), 2)

    # --- High Demand Risk ---
    high_demand_risk = df[(df["Sales 2024"] > 0) & (df["Inventory"] < df["Avg Monthly Sales"])] \
        .sort_values("Sales 2024", ascending=False)

    # --- Dead Stock ---
    dead_stock = df[(df["Inventory"] > 0) & (df["Sales 2024"] == 0)] \
        .sort_values("Inventory", ascending=False)

    # --- Out-of-Stock but High Demand ---
    out_of_stock_high_demand = df[(df["Inventory"] == 0) & (df["Sales 2024"] > 0)] \
        .sort_values("Sales 2024", ascending=False)

    # --- Slow-Moving Inventory ---
    average_sales = df["Sales 2024"].mean()
    slow_moving = df[(df["Inventory"] > 0) & (df["Sales 2024"] < average_sales)] \
        .sort_values("Inventory", ascending=False)

    # --- Zero-Zero Products ---
    stagnant_items = df[(df["Inventory"] == 0) & (df["Sales 2024"] == 0)]

    return {
        "risk_counts": risk_counts,
        "average_turnover": average_turnover,
        "risky_items": high_demand_risk,
        "dead_stock": dead_stock,
        "out_of_stock_high_demand": out_of_stock_high_demand,
        "slow_moving": slow_moving,
        "zero_zero_items": stagnant_items,
        "df_with_risk": df
    }
