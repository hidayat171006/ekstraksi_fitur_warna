
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# KONFIGURASI FOLDER
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "hasil" / "fitur_warna.csv"

# ==========================================
# KONFIGURASI FITUR
# ==========================================

RGB_FEATURES = [
    "mean_R", "mean_G", "mean_B",
    "std_R", "std_G", "std_B"
]

HSV_FEATURES = [
    "mean_H", "mean_S", "mean_V",
    "std_H", "std_S", "std_V"
]

EXPECTED_CATEGORIES = [
    "daisy",
    "dandelion",
    "rose",
    "sunflower",
    "tulip"
]

# ==========================================
# MEMBACA DATASET
# ==========================================

print("=" * 60)
print("EVALUASI HASIL EKSTRAKSI FITUR WARNA")
print("=" * 60)

print("\n[1] Membaca dataset...")

df = pd.read_csv(DATA_PATH)

print("Jumlah data:", len(df))
print("Jumlah kolom:", len(df.columns))

# ==========================================
# MEMERIKSA JUMLAH DATA
# ==========================================

print("\n[2] Memeriksa jumlah gambar...")

if len(df) == 4317:
    print("[VALID] Jumlah data sesuai: 4317 gambar")
else:
    print("[PERINGATAN] Jumlah data tidak sesuai:",
          len(df))

# ==========================================
# MEMERIKSA KATEGORI
# ==========================================

print("\n[3] Memeriksa kategori bunga...")

print(df["kategori"].value_counts())

categories = df["kategori"].dropna().unique()

for category in EXPECTED_CATEGORIES:
    if category in categories:
        print(f"[VALID] {category}")
    else:
        print(f"[TIDAK VALID] {category} tidak ditemukan")

# ==========================================
# MEMERIKSA NILAI KOSONG
# ==========================================

print("\n[4] Memeriksa missing value...")

missing = df.isnull().sum()

print(missing)

if missing.sum() == 0:
    print("[VALID] Tidak terdapat nilai kosong")
else:
    print("[PERINGATAN] Terdapat nilai kosong")

# ==========================================
# MEMERIKSA DATA DUPLIKAT
# ==========================================

print("\n[5] Memeriksa data duplikat...")

duplicates = df.duplicated().sum()

print("Jumlah data duplikat:", duplicates)

# ==========================================
# MEMERIKSA FITUR RGB
# ==========================================

print("\n[6] Memeriksa rentang nilai RGB...")

for feature in RGB_FEATURES:
    if feature not in df.columns:
        print(f"[ERROR] Kolom {feature} tidak ditemukan")
        continue

    valid = df[feature].between(0, 255).all()

    if valid:
        print(f"[VALID] {feature}")
    else:
        print(f"[TIDAK VALID] {feature}")

# ==========================================
# MEMERIKSA FITUR HSV
# ==========================================

print("\n[7] Memeriksa rentang nilai HSV...")

HSV_RANGES = {
    "mean_H": (0, 179),
    "std_H": (0, 179),
    "mean_S": (0, 255),
    "std_S": (0, 255),
    "mean_V": (0, 255),
    "std_V": (0, 255)
}

for feature, (minimum, maximum) in HSV_RANGES.items():

    if feature not in df.columns:
        print(f"[ERROR] Kolom {feature} tidak ditemukan")
        continue

    valid = df[feature].between(minimum, maximum).all()

    if valid:
        print(f"[VALID] {feature}")
    else:
        print(f"[TIDAK VALID] {feature}")

# ==========================================
# MEMERIKSA NILAI STANDAR DEVIASI
# ==========================================

print("\n[8] Memeriksa standar deviasi...")

STD_FEATURES = [
    "std_R", "std_G", "std_B",
    "std_H", "std_S", "std_V"
]

for feature in STD_FEATURES:

    if feature not in df.columns:
        print(f"[ERROR] Kolom {feature} tidak ditemukan")
        continue

    if (df[feature] >= 0).all():
        print(f"[VALID] {feature}")
    else:
        print(f"[TIDAK VALID] {feature}")

# ==========================================
# MEMERIKSA NILAI INFINITE
# ==========================================

print("\n[9] Memeriksa nilai tidak terhingga...")

numeric_df = df.select_dtypes(include=[np.number])

infinite = np.isinf(numeric_df).sum().sum()

print("Jumlah nilai infinite:", infinite)

if infinite == 0:
    print("[VALID] Tidak terdapat nilai infinite")

# ==========================================
# RINGKASAN EVALUASI
# ==========================================

print("\n" + "=" * 60)
print("RINGKASAN EVALUASI")
print("=" * 60)

print("Total gambar       :", len(df))
print("Total kategori     :", len(categories))
print("Total kolom        :", len(df.columns))
print("Missing value      :", missing.sum())
print("Data duplikat      :", duplicates)
print("Nilai infinite     :", infinite)

print("\nEvaluasi selesai!")
print("=" * 60)
