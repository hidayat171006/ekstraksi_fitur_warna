
from pathlib import Path
import pandas as pd

from src.utils.image_processing import get_image_paths, load_image
from src.extract_features import extract_color_features
from src.visualization import visualize_image


# ==========================================
# KONFIGURASI FOLDER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "dataset" / "flowers"
RESULT_DIR = BASE_DIR / "hasil"
VISUAL_DIR = RESULT_DIR / "visualisasi"


# ==========================================
# PROGRAM UTAMA
# ==========================================

def main():

    print("=" * 60)
    print("EKSTRAKSI FITUR WARNA DAN STATISTIK CITRA")
    print("=" * 60)

    # Membuat folder hasil jika belum tersedia
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    VISUAL_DIR.mkdir(parents=True, exist_ok=True)

    # Membaca seluruh gambar dalam dataset
    print("\n[1] Membaca dataset...")

    images = get_image_paths(DATASET_DIR)

    if not images:
        print("Tidak ada gambar ditemukan!")
        print("Periksa kembali folder dataset/flowers.")
        return

    print(f"Jumlah gambar ditemukan: {len(images)}")

    # Menyiapkan tempat penyimpanan fitur
    all_features = []

    # Agar visualisasi hanya dibuat satu gambar per kategori
    visualized_categories = set()

    print("\n[2] Melakukan ekstraksi fitur...")

    for index, item in enumerate(images, start=1):

        image_path = item["path"]
        category = item["category"]

        try:
            # Membaca dan mengubah ruang warna
            image_rgb, image_hsv = load_image(image_path)

            # Menghitung mean dan standard deviation
            features = extract_color_features(
                image_rgb,
                image_hsv
            )

            # Menambahkan identitas gambar
            row = {
                "nama_file": image_path.name,
                "kategori": category,
                **features
            }

            all_features.append(row)

            # Membuat visualisasi satu gambar per kategori
            if category not in visualized_categories:

                image_name = f"{category}_{image_path.name}"

                visualize_image(
                    image_rgb,
                    image_hsv,
                    image_name,
                    VISUAL_DIR
                )

                visualized_categories.add(category)

            # Menampilkan progres setiap 100 gambar
            if index % 100 == 0:
                print(
                    f"Progres: {index}/{len(images)} gambar"
                )

        except Exception as error:
            print(f"Gagal memproses {image_path.name}: {error}")

    # Memeriksa hasil ekstraksi
    if not all_features:
        print("\nTidak ada fitur yang berhasil diekstraksi.")
        return

    # Mengubah hasil menjadi DataFrame
    print("\n[3] Menyimpan hasil ekstraksi...")

    dataframe = pd.DataFrame(all_features)

    # Menyimpan ke CSV
    csv_path = RESULT_DIR / "fitur_warna.csv"
    dataframe.to_csv(csv_path, index=False)

    # Menyimpan ke Excel
    excel_path = RESULT_DIR / "fitur_warna.xlsx"
    dataframe.to_excel(excel_path, index=False)

    # Menampilkan ringkasan
    print("\n" + "=" * 60)
    print("PROSES EKSTRAKSI SELESAI")
    print("=" * 60)

    print(f"Total gambar berhasil diproses: {len(dataframe)}")
    print(f"Jumlah fitur warna: 12")

    print("\nDistribusi gambar berdasarkan kategori:")
    print(dataframe["kategori"].value_counts())

    print("\nFile hasil:")
    print(f"CSV   : {csv_path}")
    print(f"Excel : {excel_path}")
    print(f"Visualisasi : {VISUAL_DIR}")

    print("\nContoh hasil ekstraksi:")
    print(dataframe.head())

    print("\nProgram selesai!")


if __name__ == "__main__":
    main()
