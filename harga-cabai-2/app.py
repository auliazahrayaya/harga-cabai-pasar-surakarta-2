import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------
#   CONFIG HALAMAN
# ---------------------------------------------------
st.set_page_config(
    page_title="Prediksi Harga Cabai Mingguan",
    page_icon="🌶️",
    layout="wide"
)

# ---------------------------------------------------
#   CSS CUSTOM BIAR SUPER CANTIK
# ---------------------------------------------------
st.markdown("""
<style>

body {
    background: #fff8f6;
}

.header {
    background: linear-gradient(90deg, #ff3c3c, #ff7d47);
    padding: 25px; 
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.box {
    background: white;
    padding: 22px;
    border-radius: 12px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.07);
    margin-bottom: 20px;
    border-left: 5px solid #ff4d4d;
}

.result-card {
    padding: 20px;
    border-radius: 12px;
    color: white;
    margin-top: 10px;
    font-size: 20px;
    font-weight: 600;
}

.safe { background: #2ecc71; }
.warning { background: #e74c3c; }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
#   HEADER
# ---------------------------------------------------
st.markdown("""
<div class='header'>
    <h1>🌶️ Prediksi Harga Cabai Mingguan</h1>
    <h3>Interpolasi Linear • Dashboard Interaktif</h3>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------
#   LAYOUT 2 KOLOM
# ---------------------------------------------------
col1, col2 = st.columns([1, 2])

# ---------------------------------------------------
#   KOLOM KIRI (INPUT)
# ---------------------------------------------------
with col1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📥 Input Harga Bulanan (Agustus–November)")

    months = ["Agustus", "September", "Oktober", "November"]
    month_prices = {}

    for m in months:
        month_prices[m] = st.number_input(
            f"Harga rata-rata {m} (Rp)",
            value=40000,
            min_value=0
        )

    proses = st.button("🔄 Proses Prediksi", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
#   KOLOM KANAN (OUTPUT)
# ---------------------------------------------------
with col2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📊 Grafik & Prediksi Mingguan")

    if proses:

        # --------------------------
        # 1. Interpolasi Linear
        # --------------------------
        minggu_ke = np.array([1, 5, 9, 13])
        harga_bulan = np.array([
            month_prices["Agustus"],
            month_prices["September"],
            month_prices["Oktober"],
            month_prices["November"]
        ])

        minggu_full = np.arange(1, 14)
        harga_mingguan = np.interp(minggu_full, minggu_ke, harga_bulan)

        # --------------------------
        # 2. Slider Minggu
        # --------------------------
        pilih = st.slider("Pilih minggu", 1, 13, 1)
        prediksi = harga_mingguan[pilih - 1]

        # --------------------------
        # 3. Grafik
        # --------------------------
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(minggu_full, harga_mingguan, "-o", color="#ff3c3c", label="Harga Mingguan")
        ax.scatter(pilih, prediksi, s=150, color="#000", label=f"Prediksi Minggu {pilih}")
        ax.grid(alpha=0.3)
        ax.set_xlabel("Minggu")
        ax.set_ylabel("Harga (Rp)")
        ax.legend()
        ax.set_title("Prediksi Harga Cabai per Minggu")
        st.pyplot(fig)

        # --------------------------
        # 4. Hasil + Warning
        # --------------------------

        rata2 = np.mean(harga_mingguan)

        if prediksi > rata2:
            st.markdown(
                f"<div class='result-card warning'>⚠️ Harga Tinggi! Prediksi: Rp {int(prediksi):,}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='result-card safe'>🟢 Harga Aman! Prediksi: Rp {int(prediksi):,}</div>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

