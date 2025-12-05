import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ===============================
#       CONFIGURASI HALAMAN
# ===============================
st.set_page_config(
    page_title="Prediksi Harga Cabai",
    page_icon="🌶️",
    layout="wide"
)

# ===============================
#         CUSTOM CSS
# ===============================
st.markdown("""
<style>
    .title {
        font-size: 38px;
        font-weight: 800;
        color: #b30000;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #444;
        margin-bottom: 25px;
    }
    .box {
        background-color: #fff5f5;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #cc0000;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
#           HEADER
# ===============================
st.markdown("<div class='title'>🌶️ Prediksi Harga Cabai</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Menggunakan Metode Interpolasi Spline (UMKM – Metode Numerik)</div>", unsafe_allow_html=True)

st.write("")  # spasi

# ===============================
#       LAYOUT 2 KOLOM
# ===============================
col1, col2 = st.columns([1, 2])

# ===============================
#     KOLOM KIRI — INPUT DATA
# ===============================
with col1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("🔢 Input Data Harga Cabai")
    bulan = st.selectbox("Pilih Bulan", ["September", "Oktober", "November"])
    
    st.write("Masukkan data harga cabai per minggu:")

    minggu_input = st.text_input("Minggu (contoh: 1,2,3,4)", "1,2,3,4")
    harga_input = st.text_input("Harga (contoh: 38000,42000,40000,39000)", "38000,42000,40000,39000")

    proses_btn = st.button("🔄 Proses Data", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
#      KOLOM KANAN — OUTPUT
# ===============================
with col2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("📊 Grafik Prediksi & Analisis")

    if proses_btn:
        try:
            # Konversi data menjadi array
            minggu = np.array([int(x) for x in minggu_input.split(",")])
            harga = np.array([int(x) for x in harga_input.split(",")])

            # Interpolasi spline
            spline = CubicSpline(minggu, harga)

            # Slider prediksi
            pred_week = st.slider(
                f"Pilih Minggu untuk Prediksi ({bulan})",
                min(int(minggu.min())), 
                max(int(minggu.max())),
                int(minggu.min())
            )

            prediksi = spline(pred_week)

            # ===============================
            #          GRAFIK
            # ===============================
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(minggu, harga, "o-", color="#cc0000", linewidth=2, label="Data Harga")
            ax.scatter(pred_week, prediksi, s=150, color="black", label="Prediksi")
            ax.set_title(f"Grafik Prediksi Harga Cabai - {bulan}", fontweight="bold")
            ax.set_xlabel("Minggu")
            ax.set_ylabel("Harga (Rp)")
            ax.grid(True, linestyle="--", alpha=0.5)
            ax.legend()

            st.pyplot(fig)

            # ===============================
            #         WARNING HARGA
            # ===============================
            st.write("### 🚨 Hasil Analisis Harga")

            rata2 = np.mean(harga)
            hasil_int = int(prediksi)

            if hasil_int > rata2 + 3000:
                st.error(f"⚠️ **Harga Tinggi!** Diprediksi: **Rp {hasil_int:,}**\n\nWaspada kenaikan harga di minggu ini.")
            elif hasil_int < rata2 - 3000:
                st.success(f"🟢 **Harga Turun / Aman** – Rp {hasil_int:,}")
            else:
                st.warning(f"🟡 **Harga Stabil** – Rp {hasil_int:,}")

        except:
            st.error("❌ Input tidak valid! Pastikan hanya angka & koma.")

    else:
        st.info("Masukkan data lalu klik **Proses Data** untuk melihat grafik prediksi.")

    st.markdown("</div>", unsafe_allow_html=True)
