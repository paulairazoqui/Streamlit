# make_ventas.py
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

data = {
    "fecha": pd.date_range(start="2024-01-01", periods=30, freq="D"),
    "empresa": ["Empresa A"] * 15 + ["Empresa B"] * 15,
    "producto": ["Producto X", "Producto Y", "Producto Z"] * 10,
    "unidades": [5, 7, 3, 6, 8, 4, 9, 2, 5, 7, 3, 6, 8, 4, 9,
                 10, 12, 8, 15, 7, 14, 6, 13, 9, 12, 8, 11, 10, 7, 15],
    "ingreso": [500, 700, 300, 600, 800, 400, 900, 200, 500, 700,
                300, 600, 800, 400, 900, 1000, 1200, 800, 1500, 700,
                1400, 600, 1300, 900, 1200, 800, 1100, 1000, 700, 1500]
}

df = pd.DataFrame(data)
out_path = DATA_DIR / "ventas.csv"
df.to_csv(out_path, index=False)
print(f"✅ Generado: {out_path}")
