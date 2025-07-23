def generate_insight_text(kpis: dict, risks: dict) -> str:
    """
    Generate a summary insight based on calculated KPIs and inventory status.

    Args:
        kpis (dict): Output from calculate_kpis()
        risks (dict): Output from analyze_inventory()

    Returns:
        str: Insight summary in British English
    """

    total_sales = int(kpis["total_sales"])
    total_revenue = round(kpis["total_revenue"])
    gross_profit = round(kpis["gross_profit"])
    inventory_value = round(kpis["inventory_value"])

    return (
        f"In 2024, the business recorded total sales of {total_sales:,} units, generating "
        f"£{total_revenue:,} in revenue with a gross profit of approximately £{gross_profit:,}. "
        f"Current inventory value stands at £{inventory_value:,}.\n\n"
        f"These figures highlight the importance of aligning procurement with actual demand and addressing dead stock more efficiently."
    )
