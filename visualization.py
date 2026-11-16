
import matplotlib.pyplot as plt
from pathlib import Path


def visualize_image(image_rgb, image_hsv, image_name, output_dir):
    """
    Visualisasi ekstraksi fitur warna:
    1. Gambar asli
    2. Kanal RGB
    3. Kanal HSV
    4. Histogram RGB
    5. Histogram HSV
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(3, 3, figsize=(17, 13))

    try:
        # =====================================
        # GAMBAR ASLI
        # =====================================

        axes[0, 0].imshow(image_rgb)
        axes[0, 0].set_title("Gambar Asli")
        axes[0, 0].axis("off")

        # =====================================
        # KANAL RGB
        # =====================================

        rgb_labels = ["Red (R)", "Green (G)", "Blue (B)"]

        rgb_positions = [
            axes[0, 1],
            axes[0, 2],
            axes[1, 0]
        ]

        for i in range(3):

            rgb_positions[i].imshow(
                image_rgb[:, :, i],
                cmap="gray",
                vmin=0,
                vmax=255
            )

            rgb_positions[i].set_title(
                f"Kanal {rgb_labels[i]}"
            )

            rgb_positions[i].axis("off")

        # =====================================
        # KANAL HSV
        # =====================================

        hsv_labels = [
            "Hue (H)",
            "Saturation (S)",
            "Value (V)"
        ]

        hsv_colormaps = [
            "hsv",
            "gray",
            "gray"
        ]

        hsv_positions = [
            axes[1, 1],
            axes[1, 2],
            axes[2, 0]
        ]

        for i in range(3):

            max_value = 179 if i == 0 else 255

            hsv_positions[i].imshow(
                image_hsv[:, :, i],
                cmap=hsv_colormaps[i],
                vmin=0,
                vmax=max_value
            )

            hsv_positions[i].set_title(
                f"Kanal {hsv_labels[i]}"
            )

            hsv_positions[i].axis("off")

        # =====================================
        # HISTOGRAM RGB
        # =====================================

        rgb_colors = ["red", "green", "blue"]

        for i in range(3):

            axes[2, 1].hist(
                image_rgb[:, :, i].ravel(),
                bins=256,
                range=(0, 256),
                color=rgb_colors[i],
                alpha=0.4,
                label=rgb_labels[i]
            )

        axes[2, 1].set_title("Histogram RGB")
        axes[2, 1].set_xlabel("Intensitas Piksel")
        axes[2, 1].set_ylabel("Jumlah Piksel")
        axes[2, 1].legend()
        axes[2, 1].grid(alpha=0.2)

        # =====================================
        # HISTOGRAM HSV
        # =====================================

        hsv_colors = ["orange", "purple", "gray"]

        for i in range(3):

            bins = 180 if i == 0 else 256
            value_range = (0, 180) if i == 0 else (0, 256)

            axes[2, 2].hist(
                image_hsv[:, :, i].ravel(),
                bins=bins,
                range=value_range,
                color=hsv_colors[i],
                alpha=0.4,
                label=hsv_labels[i]
            )

        axes[2, 2].set_title("Histogram HSV")
        axes[2, 2].set_xlabel("Nilai Kanal")
        axes[2, 2].set_ylabel("Jumlah Piksel")
        axes[2, 2].legend()
        axes[2, 2].grid(alpha=0.2)

        # =====================================
        # JUDUL DAN PENYIMPANAN
        # =====================================

        plt.suptitle(
            f"Analisis Ekstraksi Fitur Warna: {image_name}",
            fontsize=15,
            fontweight="bold"
        )

        plt.tight_layout(rect=[0, 0, 1, 0.96])

        safe_name = Path(image_name).stem

        save_path = output_dir / f"{safe_name}_visualisasi.png"

        fig.savefig(
            save_path,
            dpi=200,
            bbox_inches="tight"
        )

        return save_path

    finally:
        # Selalu menutup figure meskipun terjadi error
        plt.close(fig)
