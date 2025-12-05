import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================
#   SETTING HALAMAN
# ==========================
st.set_page_config(
    page_title="Prediksi Harga Cabai",
    page_icon="🌶️",
    layout="wide"
)

# ==========================
#   CSS AESTHETIC
# ==========================
st.markdown("""
<style>
    body {
        background-color: #fafafa;
    }
    .header-box {
        background: linear-gradient(90deg, #ff4d4d, #b30000);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .sub-box {
        background: #ffffffcc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
#   HEADER
# ==========================
st.markdown("<div class='header-box'><h1>🌶️ Prediksi Harga Cabai Mingguan</h1><p>Interpolasi Linear – Data UMKM</p></div>", unsafe_allow_html=True)

# ==========================
#   DATA PER BULAN
# ==========================
data_bulanan = {
    "Agustus": [38000, 40000, 39000, 41000],
    "September": [42000, 43000, 41500, 44000],
    "Oktober": [45000, 47000, 46000, 48000],
    "November": [49000, 51000, 50000, 52000]
}

# ==========================
#   LAYOUT
# ==========================
col1, col2 = st.columns([1, 2])

# ==========================
#   KOLOM 1 — INPUT
# ==========================
with col1:
    st.markdown("<div class='sub-box'>", unsafe_allow_html=True)
    st.subheader("🗓️ Pilih Bulan & Minggu")

    bulan = st.selectbox("Pilih Bulan", list(data_bulanan.keys()))
    minggu = st.slider("Minggu ke-", 1, 4, 1)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
#   PROSES DATA
# ==========================
harga_mingguan = data_bulanan[bulan]

# Interpolasi Linear sederhana
minggu_x = np.array([1,2,3,4])
harga_y = np.array(harga_mingguan)
prediksi = np.interp(minggu, minggu_x, harga_y)

# ==========================
#   KOLOM 2 — OUTPUT
# ==========================
with col2:
    st.markdown("<div class='sub-box'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Prediksi")

    # GRAFIK
    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(minggu_x, harga_y, "o-", color="#cc0000", linewidth=2)
    ax.scatter(minggu, prediksi, s=150, color="black", label=f"Prediksi Minggu {minggu}")
    ax.set_xlabel("Minggu")
    ax.set_ylabel("Harga (Rp)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.set_title(f"Grafik Harga Cabai – {bulan}")

    st.pyplot(fig)

    # ALERT
    st.write("### 🔍 Analisis Harga")
    if prediksi > np.mean(harga_y):
        st.error(f"⚠️ Harga diprediksi TINGGI: **Rp {int(prediksi):,}**")
    else:
        st.success(f"Harga diprediksi AMAN: **Rp {int(prediksi):,}**")

    st.markdown("</div>", unsafe_allow_html=True)
