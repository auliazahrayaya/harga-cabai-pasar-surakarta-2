import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Page config
# -------------------------
st.set_page_config(
    page_title="Prediksi Harga Cabai di Jawa Tengah untuk UMKM",
    page_icon="🌶️",
    layout="wide"
)

# -------------------------
# Styling (simple & neat)
# -------------------------
st.markdown("""
<style>
  body { background-color: #fff9f8; }
  .header {
    background: linear-gradient(90deg,#ff4d4d,#ff8a5c);
    color: white;
    padding: 18px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    margin-bottom: 20px;
  }
  .card {
    background: white;
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 16px;
  }
  .tip {
    background: #fff4f2;
    border-left: 5px solid #ff6b4d;
    padding: 12px;
    border-radius: 8px;
  }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header (title + tagline you asked)
# -------------------------
st.markdown("""
<div class="header">
  <h1 style="margin:0;">🌶️ Prediksi Harga Cabai di Jawa Tengah untuk UMKM</h1>
  <div style="opacity:0.95; margin-top:6px;">Aplikasi visual untuk membantu UMKM memantau harga mingguan dan mengambil keputusan belanja</div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Default weekly data per month (editable)
# -------------------------
default_data = {
    "Agustus":   [35000, 36000, 37000, 36500],
    "September": [38000, 42000, 40000, 39000],
    "Oktober":   [41000, 43000, 44500, 42000],
    "November":  [45000, 47000, 46000, 45500]
}

# -------------------------
# Layout: left = controls, right = output
# -------------------------
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Input & Pengaturan Data")
    st.write("Pilih bulan, sesuaikan nilai mingguan (opsional).")

    # month selector
    month = st.selectbox("Pilih Bulan", list(default_data.keys()))

    # show editable weekly values in expander
    with st.expander("Lihat / Edit data mingguan (opsional)"):
        w1 = st.number_input("Minggu 1 (Rp)", value=int(default_data[month][0]), min_value=0, step=500)
        w2 = st.number_input("Minggu 2 (Rp)", value=int(default_data[month][1]), min_value=0, step=500)
        w3 = st.number_input("Minggu 3 (Rp)", value=int(default_data[month][2]), min_value=0, step=500)
        w4 = st.number_input("Minggu 4 (Rp)", value=int(default_data[month][3]), min_value=0, step=500)

    st.write("---")
    st.caption("Gunakan slider di kanan untuk memilih minggu (bisa berangka desimal untuk interpolasi linear).")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Grafik & Prediksi Mingguan")

    # prepare arrays (use edited values if changed)
    xp = np.array([1, 2, 3, 4], dtype=float)
    yp = np.array([w1, w2, w3, w4], dtype=float)

    # slider: allow fractional (interpolate between weeks)
    week = st.slider("Pilih minggu (1.0 = Minggu 1, 2.5 = tengah Minggu 2-3)", min_value=1.0, max_value=4.0, value=1.0, step=0.1)

    # linear interpolation using numpy.interp
    pred_price = float(np.interp(week, xp, yp))

    # plot (smooth line by interpolation points)
    xs = np.linspace(1, 4, 200)
    ys = np.interp(xs, xp, yp)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(xs, ys, color="#d94b3b", linewidth=2, label="Perkiraan Harga (linear)")
    ax.plot(xp, yp, 'o', color="#b30000", markersize=8, label="Data Mingguan (input)")
    ax.scatter(week, pred_price, color="black", s=120, zorder=5, label=f"Prediksi (minggu {week:.1f})")
    ax.set_xlabel("Minggu")
    ax.set_ylabel("Harga (Rp)")
    ax.set_title(f"Harga Mingguan — {month}")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend()
    st.pyplot(fig)

    # display numeric results
    st.write("**Prediksi Harga:**", f"Rp {int(round(pred_price)):,}")

    # -------------------------
    # Warning logic (UMKM-friendly text)
    # -------------------------
    avg = np.mean(yp)
    diff = pred_price - avg

    # thresholds: tweakable
    if diff > 3000:
        # High: strong warning and UMKM actions
        st.error(f"⚠️ Harga diprediksi *TINGGI* (Rp {int(round(pred_price)):,}).")
        st.markdown("""
        **Rekomendasi cepat untuk UMKM (Surakarta):**
        - Tunda pembelian stok besar, beli secukupnya untuk 1–2 hari.  
        - Cek beberapa pemasok lokal untuk bandingkan harga.  
        - Pertimbangkan pembelian bersama (gabungan) dengan pelaku UMKM lain untuk mendapatkan harga grosir.
        - Evaluasi menu: kurangi porsi cabai atau gunakan substitusi sementara.
        """)
    elif diff > 0:
        # Slightly above average: caution
        st.warning(f"🟡 Harga diprediksi sedikit di atas rata‑rata (Rp {int(round(pred_price)):,}).")
        st.markdown("""
        **Saran praktis untuk UMKM:**
        - Beli stok untuk 2–3 hari, pantau harga harian.  
        - Siapkan daftar pemasok cadangan dan catat harga tiap pasar.  
        """)
    else:
        # Below or equal avg: safe
        st.success(f"🟢 Harga diprediksi *STABIL / AMAN* (Rp {int(round(pred_price)):,}).")
        st.markdown("""
        **Manfaat untuk UMKM:**
        - Bisa membeli stok 3–5 hari.  
        - Gunakan saat ini untuk rencanakan menu & promosi.  
        - Simpan sebagian stok dengan teknik pendinginan sederhana.
        """)

    # -------------------------
    # Optional: show table & download
    # -------------------------
    st.write("---")
    st.subheader("Data Mingguan (tabel)")
    df = pd.DataFrame({
        "Minggu": ["1","2","3","4"],
        "Harga (Rp)": [int(yp[0]), int(yp[1]), int(yp[2]), int(yp[3])]
    })
    st.dataframe(df, width=400)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download data mingguan (CSV)", data=csv, file_name=f"harga_mingguan_{month}.csv", mime="text/csv")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Footer tips (small)
# -------------------------
st.markdown("""
<div style="margin-top:12px; font-size:13px; color:#555;">
  Catatan: ini adalah estimasi sederhana (interpolasi linear antar-minggu). Bila ingin prediksi jangka panjang
  atau otomatis dari data historis pasar, bisa gunakan model time-series (opsional).
</div>
""", unsafe_allow_html=True)


