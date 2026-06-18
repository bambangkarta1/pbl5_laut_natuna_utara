import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Estimasi Stok Ikan Natuna", layout="wide")
st.title("🐟 Estimasi Stok Ikan Laut Natuna Utara (2025)")

# Data (sudah urut bulan)
data = {
    "Bulan": ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Ags","Sep","Okt","Nov","Des"],
    "SST (°C)": [27.49,26.77,28.44,29.96,31.10,30.84,30.16,30.51,30.38,30.43,30.44,28.74],
    "Klorofil (mg/m³)": [0.43,0.31,0.26,0.22,0.21,0.29,0.30,0.31,0.32,0.26,0.27,0.35]
}
df = pd.DataFrame(data)

def estimasi_stok(sst, klorofil):
    return 5000 * klorofil - 100 * (sst - 29)**2 + 2000

df["Stok (ton)"] = df.apply(lambda row: estimasi_stok(row["SST (°C)"], row["Klorofil (mg/m³)"]), axis=1)

# Tabel
st.subheader("📋 Data Bulanan")
st.dataframe(df.style.format({"SST (°C)": "{:.2f}", "Klorofil (mg/m³)": "{:.2f}", "Stok (ton)": "{:,.0f}"}),
             use_container_width=True, height=350)

# Sidebar input manual
st.sidebar.header("🔧 Estimasi Manual")
sst_in = st.sidebar.number_input("SST (°C)", 25.0, 33.0, 29.0, 0.1)
klo_in = st.sidebar.number_input("Klorofil (mg/m³)", 0.0, 5.0, 0.3, 0.01)
if st.sidebar.button("Hitung"):
    st.sidebar.success(f"Stok: {estimasi_stok(sst_in, klo_in):,.0f} ton")
else:
    st.sidebar.info("Masukkan nilai lalu klik tombol.")
    st.sidebar.markdown("---")

# Logo UNISBA
st.sidebar.image("logo-unisba.png", width=100)

st.sidebar.markdown("""
**Kelompok 6**

Arif Hamdani  
10090224008

Bambang Karta Wijaya  
10090224025

Moh Bayu Mustofa  
10090224030

Ekonomi Pembangunan | UNISBA | 2026
""")

# Pilihan grafik
st.subheader("📈 Pilih Tampilan Grafik")
tampilan = st.selectbox("Jenis grafik:", [
    "Tren Bulanan (garis)",
    "SST vs Stok (scatter + garis)",
    "Klorofil vs Stok (scatter + garis)"
])

if tampilan == "Tren Bulanan (garis)":
    # Grafik garis dengan sumbu x = bulan (kronologis)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Bulan"], y=df["SST (°C)"], mode="lines+markers",
                             name="SST (°C)", yaxis="y", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Klorofil (mg/m³)"], mode="lines+markers",
                             name="Klorofil (mg/m³)", yaxis="y2", line=dict(width=2)))
    fig.add_trace(go.Scatter(x=df["Bulan"], y=df["Stok (ton)"], mode="lines+markers",
                             name="Stok (ton)", yaxis="y3", line=dict(width=2)))
    fig.update_layout(
        title="Perbandingan SST, Klorofil, dan Stok per Bulan",
        xaxis=dict(title="Bulan", tickangle=0),
        yaxis=dict(title="SST (°C)", side="left"),
        yaxis2=dict(title="Klorofil (mg/m³)", overlaying="y", side="right"),
        yaxis3=dict(title="Stok (ton)", overlaying="y", side="right", anchor="free", position=0.95),
        legend=dict(x=1.05, y=1),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

elif tampilan == "SST vs Stok (scatter + garis)":
    # Data diurutkan berdasarkan SST (agar garis tidak kusut)
    df_sorted = df.sort_values("SST (°C)")
    fig = px.scatter(df_sorted, x="SST (°C)", y="Stok (ton)", text="Bulan",
                     title="Hubungan SST dengan Stok (urutan berdasarkan SST)")
    fig.update_traces(textposition="top center", mode="lines+markers", line=dict(dash="dot"))
    st.plotly_chart(fig, use_container_width=True)

else:  # Klorofil vs Stok
    df_sorted = df.sort_values("Klorofil (mg/m³)")
    fig = px.scatter(df_sorted, x="Klorofil (mg/m³)", y="Stok (ton)", text="Bulan",
                     title="Hubungan Klorofil dengan Stok (urutan berdasarkan Klorofil)")
    fig.update_traces(textposition="top center", mode="lines+markers", line=dict(dash="dot"))
    st.plotly_chart(fig, use_container_width=True)

# Info model
with st.expander("ℹ️ Model"):
    st.markdown("Stok = 5000×Klorofil − 100×(SST−29)² + 2000")
