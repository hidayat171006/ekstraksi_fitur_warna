
import cv2
from pathlib import Path


# Format gambar yang didukung
SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


def get_image_paths(dataset_path):
    """
    Mengambil seluruh lokasi gambar dari setiap kategori dataset.
    """

    dataset_path = Path(dataset_path)

    image_data = []

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Folder dataset tidak ditemukan: {dataset_path}"
        )

    for category_folder in sorted(dataset_path.iterdir()):

        if not category_folder.is_dir():
            continue

        category = category_folder.name

        for image_path in sorted(category_folder.iterdir()):

            if image_path.suffix.lower() in SUPPORTED_EXTENSIONS:

                image_data.append({
                    "path": image_path,
                    "category": category
                })

    return image_data


def load_image(image_path):
    """
    Membaca gambar dan mengubahnya menjadi RGB dan HSV.
    """

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(
            f"Gambar gagal dibaca: {image_path}"
        )

    # Mengubah BGR menjadi RGB
    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Mengubah BGR menjadi HSV
    image_hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    return image_rgb, image_hsv
