
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# KONFIGURASI FOLDER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "hasil" / "fitur_warna.csv"
OUTPUT_DIR = BASE_DIR / "hasil" / "analisis"


# ==========================================
# DAFTAR FITUR
# ==========================================

RGB_FEATURES = [
    "mean_R", "mean_G", "mean_B"
]

HSV_FEATURES = [
    "mean_H", "mean_S", "mean_V"
]

RGB_STD = [
    "std_R", "std_G", "std_B"
]

HSV_STD = [
    "std_H", "std_S", "std_V"
]


# ==========================================
# FUNGSI MEMBUAT GRAFIK
# ==========================================

def create_chart(data, columns, title, ylabel, filename):

    ax = data[columns].plot(
        kind="bar",
        figsize=(12, 6),
        width=0.8
    )

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Kategori Bunga")
    ax.set_ylabel(ylabel)

    ax.legend(title="Fitur")
    ax.grid(axis="y", alpha=0.3)

    plt.xticks(rotation=0)
    plt.tight_layout()

    save_path = OUTPUT_DIR / filename

    plt.savefig(
        save_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Grafik tersimpan: {save_path}")


# ==========================================
# PROGRAM UTAMA
# ==========================================

def main():

    print("=" * 60)
    print("ANALISIS STATISTIK FITUR WARNA CITRA")
    print("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Membaca hasil ekstraksi
    print("\n[1] Membaca dataset fitur...")

    if not DATA_PATH.exists():
        print("File fitur_warna.csv tidak ditemukan!")
        return

    df = pd.read_csv(DATA_PATH)

    print(f"Jumlah data: {len(df)}")

    # Memeriksa kolom fitur
    required_columns = (
        ["kategori"] +
        RGB_FEATURES +
        HSV_FEATURES +
        RGB_STD +
        HSV_STD
    )

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("Kolom tidak ditemukan:", missing_columns)
        return

    # Menghitung jumlah gambar per kategori
    print("\n[2] Menghitung jumlah gambar...")

    jumlah_gambar = df.groupby("kategori").size()

    print(jumlah_gambar)

    # Menghitung rata-rata fitur
    print("\n[3] Menghitung Mean setiap kategori...")

    mean_result = df.groupby("kategori")[
        RGB_FEATURES + HSV_FEATURES
    ].mean()

    print("\nHasil Mean:")
    print(mean_result.round(2))

    # Menghitung rata-rata standar deviasi
    print("\n[4] Menghitung Standard Deviation...")

    std_result = df.groupby("kategori")[
        RGB_STD + HSV_STD
    ].mean()

    print("\nHasil Standard Deviation:")
    print(std_result.round(2))

    # Menyimpan hasil statistik
    print("\n[5] Menyimpan hasil analisis...")

    mean_result.to_csv(
        OUTPUT_DIR / "rata_rata_fitur.csv"
    )

    std_result.to_csv(
        OUTPUT_DIR / "standar_deviasi_fitur.csv"
    )

    # Menyimpan Excel dengan beberapa sheet
    with pd.ExcelWriter(
        OUTPUT_DIR / "hasil_analisis_statistik.xlsx"
    ) as writer:

        jumlah_gambar.rename(
            "jumlah_gambar"
        ).to_frame().to_excel(
            writer,
            sheet_name="Jumlah Gambar"
        )

        mean_result.to_excel(
            writer,
            sheet_name="Rata-rata Mean"
        )

        std_result.to_excel(
            writer,
            sheet_name="Rata-rata STD"
        )

    # ======================================
    # MEMBUAT 4 GRAFIK PERBANDINGAN
    # ======================================

    print("\n[6] Membuat visualisasi statistik...")

    create_chart(
        mean_result,
        RGB_FEATURES,
        "Perbandingan Mean RGB",
        "Nilai Mean",
        "perbandingan_mean_rgb.png"
    )

    create_chart(
        mean_result,
        HSV_FEATURES,
        "Perbandingan Mean HSV",
        "Nilai Mean",
        "perbandingan_mean_hsv.png"
    )

    create_chart(
        std_result,
        RGB_STD,
        "Perbandingan Standard Deviation RGB",
        "Nilai Standard Deviation",
        "perbandingan_std_rgb.png"
    )

    create_chart(
        std_result,
        HSV_STD,
        "Perbandingan Standard Deviation HSV",
        "Nilai Standard Deviation",
        "perbandingan_std_hsv.png"
    )

    # ======================================
    # RINGKASAN
    # ======================================

    print("\n" + "=" * 60)
    print("ANALISIS STATISTIK SELESAI")
    print("=" * 60)

    print(f"Total gambar dianalisis: {len(df)}")
    print(f"Jumlah kategori: {df['kategori'].nunique()}")

    print("\nLokasi hasil:")
    print(OUTPUT_DIR)

    print("\nProgram selesai!")


if __name__ == "__main__":
    main()
