import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===============================
#  CONFIG HALAMAN
# ===============================
st.set_page_config(
    page_title="Prediksi Harga Cabai UMKM",
    page_icon="🌶️",
    layout="wide"
)

# ===============================
#  CSS TAMPILAN
# ===============================
st.markdown("""
    <style>
        body {
            background-color: #fffafa;
        }
        .header {
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            background: linear-gradient(90deg, #ff4b4b, #ff8f8f);
            color: white;
            margin-bottom: 25px;
        }
        .section {
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid #ff4b4b;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
#  HEADER
# ===============================
st.markdown("""
<div class='header'>
    <h1>🌶️ Prediksi Harga Cabai untuk UMKM</h1>
    <p>Membantu UMKM mengatur strategi belanja cabai berdasarkan interpolasi mingguan</p>
</div>
""", unsafe_allow_html=True)

# ===============================
#  DATA HARGA BULANAN → MINGGUAN
# ===============================

data_harga = {
    "Agustus":  [35000, 36000, 37000, 36500],
    "September":[38000, 42000, 40000, 39000],
    "Oktober":  [41000, 43000, 44500, 42000],
    "November": [45000, 47000, 46000, 45500]
}

# ===============================
#  KOLOM INPUT
# ===============================
col1, col2 = st.columns([1,2])

with col1:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🗓️ Pilih Bulan & Minggu")
    
    bulan = st.selectbox("Pilih Bulan:", list(data_harga.keys()))
    minggu = st.slider("Minggu ke:", 1, 4, 1)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
#  PREDIKSI (INTERPOLASI LINEAR)
# ===============================
with col2:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📊 Grafik Harga & Prediksi Mingguan")

    harga_bulanan = data_harga[bulan]
    x = np.array([1, 2, 3, 4])
    y = np.array(harga_bulanan)

    # Interpolasi linear manual
    if minggu == 1:
        pred = y[0]
    else:
        m = (y[minggu-1] - y[minggu-2]) / (1)
        pred = y[minggu-2] + m

    # Grafik
    fig, ax = plt.subplots(figsize=(7,4))
    ax.plot(x, y, "o-r", label="Data Harga per Minggu")
    ax.scatter(minggu, pred, s=120, color="black", label=f"Prediksi Minggu {minggu}")
    ax.set_xlabel("Minggu")
    ax.set_ylabel("Harga (Rp)")
    ax.set_title(f"Grafik Harga Cabai - {bulan}")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    # ===============================
    #  WARNING UNTUK UMKM
    # ===============================
    st.subheader("⚠️ Peringatan & Rekomendasi UMKM")

    rata2 = np.mean(y)
    pred_int = int(pred)

    if pred_int > rata2:
        st.error(f"⚠️ Harga Minggu {minggu} diprediksi **TINGGI**: Rp {pred_int:,}")
        st.write("""
        **💡 Rekomendasi UMKM:**
        - Kurangi pembelian stok besar.
        - Cari pemasok alternatif dengan harga lebih stabil.
        - Gunakan cabai secukupnya untuk menu harian.
        """)
    else:
        st.success(f"👍 Harga Minggu {minggu} diprediksi **STABIL**: Rp {pred_int:,}")
        st.write("""
        **💡 Tips UMKM:**
        - Bisa membeli stok untuk 3–4 hari.
        - Manfaatkan harga stabil untuk persiapan menu.
        - Simpan cabai di kertas/kulkas agar awet.
        """)

    st.markdown("</div>", unsafe_allow_html=True)

