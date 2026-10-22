import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
input_file = project_root / "data" / "raw" / "sales_raw.csv"

df = pd.read_csv(input_file)

df.columns = df.columns.str.strip().str.lower()
text_columns = ["customer_name", "product", "category"]

for column in text_columns:
    df[column] = df[column].str.strip()
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)
df = df.drop_duplicates(subset=["order_id"])
df = df[df["quantity"] > 0]
required_columns = [
    "order_id",
    "customer_id",
    "product",
    "quantity",
    "price",
    "order_date"
]

df = df.dropna(subset=required_columns)
df["sales_amount"] = df["quantity"] * df["price"]
print(df)
output_file = project_root / "data" / "processed" / "sales_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nCleaned data saved to: {output_file}")