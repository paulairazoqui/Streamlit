# app.py
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from pathlib import Path

st.set_page_config(page_title="Informe Empresa", layout="wide")

# -------- Ruta fija (relativa al proyecto) --------
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "ventas.csv"   # poné tu archivo acá

# -------- Carga con cache --------
@st.cache_data(show_spinner=True)
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Ajustes típicos (adaptá a tus columnas)
    # Espera columnas: fecha, empresa, producto, unidades, ingreso
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["anio_mes"] = df["fecha"].dt.to_period("M").dt.to_timestamp()
    return df

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"No pude leer el dataset en {DATA_PATH}\n{e}")
    st.stop()

# -------- Sidebar (filtros) --------
st.sidebar.header("Filtros")
empresas = sorted(df["empresa"].dropna().unique().tolist())
empresa = st.sidebar.selectbox("Empresa", options=empresas)
min_d, max_d = df["fecha"].min(), df["fecha"].max()
rango = st.sidebar.date_input("Rango de fechas", value=[min_d, max_d])
if isinstance(rango, list) and len(rango) == 2:
    d1, d2 = pd.to_datetime(rango[0]), pd.to_datetime(rango[1])
else:
    d1, d2 = min_d, max_d

df_f = df[(df["empresa"] == empresa) & (df["fecha"].between(d1, d2))]

# -------- KPIs --------
col1, col2, col3 = st.columns(3)
ingreso_total = float(df_f["ingreso"].sum()) if not df_f.empty else 0.0
unidades_total = int(df_f["unidades"].sum()) if not df_f.empty else 0
ticket_prom = ingreso_total / max(unidades_total, 1)

col1.metric("Ingreso total", f"${ingreso_total:,.0f}")
col2.metric("Unidades vendidas", f"{unidades_total:,}")
col3.metric("Ticket prom.", f"${ticket_prom:,.0f}")

st.divider()

# -------- Series & tablas --------
st.subheader(f"Evolución mensual - {empresa}")
serie = df_f.groupby("fecha", as_index=False)["ingreso"].sum()
if serie.empty:
    st.info("No hay datos para los filtros seleccionados.")
else:
    st.line_chart(serie, x="fecha", y="ingreso", height=320)

st.subheader("Detalle (filtrado)")
st.dataframe(df_f.sort_values("fecha"), use_container_width=True)

# -------- Descargas --------
st.sidebar.subheader("Descargas")
csv_buf = df_f.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("⬇️ Exportar CSV filtrado", data=csv_buf, file_name=f"informe_{empresa}.csv", mime="text/csv")

# Exportar gráfico como imagen (opcional rápido)
if not serie.empty:
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(serie["fecha"], serie["ingreso"])
    ax.set_title(f"Ingreso mensual - {empresa}")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Ingreso")
    img_buf = BytesIO()
    fig.savefig(img_buf, format="png", bbox_inches="tight")
    img_buf.seek(0)
    st.sidebar.download_button("🖼️ Descargar gráfico PNG", data=img_buf, file_name=f"ingreso_mensual_{empresa}.png", mime="image/png")
