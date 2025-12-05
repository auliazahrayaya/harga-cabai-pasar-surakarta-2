import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =======================
#  PENGATURAN HALAMAN
# =======================
st.set_page_config(
    page_title="Prediksi Harga Cabai",
    page_icon="🌶️",
    layout="wide"
)

# =======================
#   CSS BIAR PROFESIONAL
# =======================
st.markdown("""
<style>
.main-title{
    font-size: 32px;
    text-align: center;
    font-weight: bold;
    color: #b30000;
}
.sub-title{
    text-align: center;
    color: #444;
    margin-bottom: 20px;
}
.box{
    background:#fff5f5;
    padding:18px;
    border-radius:10px;
    border-left:5px solid #cc0000;
}
</style>
""", unsafe_allow_html=True)

# =======================
#   JUDUL
# =======================
st.markdown("<div class='main-title'>🌶️ Prediksi Harga Cabai - Interpolasi Linear</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Metode Numerik • Data UMKM (Per Minggu)</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

# =====================================================
#                     KOLOM KIRI
# =====================================================
with col1:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Input Data Harga Cabai")

    minggu_raw = st.text_input("Minggu (misal: 1,2,3,4)", "1,2,3,4")
    harga_raw = st.text_input("Harga (misal: 38000,42000,40000,39000)", "38000,42000,40000,39000")

    proses = st.button("Proses Data", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
#                     KOLOM KANAN
# =====================================================
with col2:
    st.markdown("<div class='box'>", unsafe_allow_html=True)
    st.subheader("Hasil Prediksi dan Grafik")

    if proses:
        try:
            # Ubah input menjadi array
            minggu = np.array([int(i) for i in minggu_raw.split(",")])
            harga = np.array([int(i) for i in harga_raw.split(",")])

            # Slider prediksi (minggu user)
            minggu_pred = st.slider(
                "Pilih minggu yang ingin diprediksi:",
                int(minggu.min()),
                int(minggu.max()),
                int(minggu.min())
            )

            # ===================================
            #     INTERPOLASI LINEAR MANUAL
            # ===================================
            def linear_interpolation(x, xp, yp):
                for i in range(len(xp)-1):
                    if xp[i] <= x <= xp[i+1]:
                        x0, x1 = xp[i], xp[i+1]
                        y0, y1 = yp[i], yp[i+1]
                        # rumus interpolasi linear
                        return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
                return None

            prediksi = linear_interpolation(minggu_pred, minggu, harga)

            if prediksi is None:
                st.error("Minggu yang dipilih berada di luar jangkauan data!")
            else:
                prediksi_int = int(prediksi)

                # ==========================
                #     GRAFIK
                # ==========================
                fig, ax = plt.subplots(figsize=(6,4))
                ax.plot(minggu, harga, "o-", label="Data Asli", color="#cc0000")
                ax.scatter(minggu_pred, prediksi_int, color="black", s=100, label="Prediksi")
                ax.set_xlabel("Minggu")
                ax.set_ylabel("Harga (Rp)")
                ax.set_title("Grafik Harga Cabai")
                ax.grid(True, linestyle="--", alpha=0.4)
                ax.legend()

                st.pyplot(fig)

                # ==========================
                #     WARNING HARGA
                # ==========================
                st.write("### Hasil Prediksi")

                rata2 = np.mean(harga)

                if prediksi_int > rata2:
                    st.error(f"⚠️ Harga diprediksi TINGGI: Rp {prediksi_int:,}")
                else:
                    st.success(f"Harga diprediksi AMAN: Rp {prediksi_int:,}")

        except:
            st.error("Format input salah. Gunakan angka dan koma.")

    else:
        st.info("Masukkan data terlebih dahulu untuk melihat hasil.")

    st.markdown("</div>", unsafe_allow_html=True)

