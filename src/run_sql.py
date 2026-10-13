
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "pharma_analytics.db"


query = """

SELECT
    p.product_name,
    i.closing_stock_units,
    i.reorder_level_units,
    CASE
        WHEN i.closing_stock_units <= i.reorder_level_units
        THEN 'Reorder Required'
        ELSE 'Stock Available'
    END AS inventory_status
FROM inventory AS i
JOIN products AS p
    ON i.product_id = p.product_id
ORDER BY i.closing_stock_units ASC;

"""
with sqlite3.connect(DB_PATH) as conn:
    result = pd.read_sql_query(query, conn)


print("\nDATABASE TABLES:")
print(result.to_string(index=False))



import plotly.express as px


fig = px.bar(
    result,
    x="product_name",
    y="closing_stock_units",
    color="inventory_status",
    barmode="group",
    title="Pharmaceutical Inventory Risk Analysis",
    labels={
        "product_name": "Medicine",
        "closing_stock_units": "Closing Stock (Units)",
        "inventory_status": "Stock Status"
    },
    hover_data=["reorder_level_units"],
    color_discrete_map={
        "Reorder Required": "#E74C3C",
        "Stock Available": "#27AE60"
    }
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Medicine",
    yaxis_title="Closing Stock (Units)",
    legend_title="Inventory Status",
    xaxis_tickangle=-30
)

fig.show()
