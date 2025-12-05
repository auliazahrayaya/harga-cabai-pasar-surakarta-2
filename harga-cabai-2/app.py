import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
#   CONFIGURASI HALAMAN
# -----------------------------
st.set_page_config(
    page_title="Prediksi Harga Cabai Mingguan",
    page_icon="🌶️",
    layout="wide"
)

# ==================== CSS BIAR KEREN ====================
st.markdown("""
<style>
    .title {
        font-size: 35px;
        font-weight: 700;
        color: #b30000;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #333;
        margin-bottom: 25px;
    }
    .box {
        background-color: #fff5f5;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #cc0000;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== JUDUL ====================
st.markdown("<div class='title'>🌶️ Prediksi Harga Cabai Mingguan</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Interpolasi Linear – Data Bulanan → Mingguan</div>", unsafe_allow_html=True)
st.write("")

# ==================== LAYOUT ====================
col1, col2 = st.columns([1, 2])

# =========================================================
#   KOLOM KIRI — INPUT DATA
# =========================================================
with col1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📥 Input Data Bulanan")

    months = ["Agustus", "September", "Oktober", "November"]
    month_prices = {}

    for m in months:
        month_prices[m] = st.number_input(
            f"Harga rata-rata {m} (Rp)",
            min_value=0,
            value=40000
        )

    process = st.button("🔄 Proses Prediksi Mingguan", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
#   KOLOM KANAN — OUTPUT
# =========================================================
with col2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📊 Hasil Prediksi Mingguan")

    if process:

        # ---------------------------
        # 1. Data Bulanan → Mingguan
        # ---------------------------
        minggu_ke = np.array([1, 5, 9, 13])  # minggu ke-1 tiap bulan
        harga_bulan = np.array([
            month_prices["Agustus"],
            month_prices["September"],
            month_prices["Oktober"],
            month_prices["November"],
        ])

        # Interpolasi linear
        minggu_full = np.arange(1, 14)
        harga_mingguan = np.interp(minggu_full, minggu_ke, harga_bulan)

        # ---------------------------
        # 2. Slider Prediksi
        # ---------------------------
        pilih_minggu = st.slider("Pilih minggu untuk memprediksi", 1, 13, 1)
        harga_prediksi = harga_mingguan[pilih_minggu - 1]

        # ---------------------------
        # 3. Grafik
        # ---------------------------
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(minggu_full, harga_mingguan, "-o", color="#cc0000", label="Harga per Minggu")
        ax.scatter(pilih_minggu, harga_prediksi, color="black", s=120, label=f"Prediksi Minggu {pilih_minggu}")
        ax.set_xlabel("Minggu")
        ax.set_ylabel("Harga (Rp)")
        ax.set_title("Prediksi Harga Cabai Mingguan")
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()
        st.pyplot(fig)

        # ---------------------------
        # 4. Warning Harga
        # ---------------------------
        st.subheader("🔍 Analisis Harga")

        avg = np.mean(harga_mingguan)
        if harga_prediksi > avg:
            st.error(f"⚠️ Harga Minggu {pilih_minggu} **TINGGI**: Rp {int(harga_prediksi):,}")
        else:
            st.success(f"Harga Minggu {pilih_minggu} **AMAN**: Rp {int(harga_prediksi):,}")

    st.markdown("</div>", unsafe_allow_html=True)

