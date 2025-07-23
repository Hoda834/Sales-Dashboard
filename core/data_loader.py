import pandas as pd
import os

def load_and_prepare_data(file_path):
    """
    Load and clean Volvo inventory & sales data.
    
    Args:
        file_path (str): Path to CSV file.
    
    Returns:
        pd.DataFrame: Cleaned and ready for analysis.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)

    # حذف ستون‌های بدون نام (مثل Unnamed: 12)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # حذف فاصله اضافی از نام ستون‌ها
    df.columns = df.columns.str.strip()

    # ستون‌هایی که باید به عدد تبدیل شوند
    numeric_cols = ["Price", "Cost", "Sales 2024", "Sales 2023", "Inventory", "Annual Target", "Order"]
    
    for col in numeric_cols:
        if col in df.columns:
            # حذف کاما، فاصله، و تبدیل به عدد
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # جایگزینی NaN با 0
    df = df.fillna(0)

    return df
