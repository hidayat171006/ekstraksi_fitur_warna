
import numpy as np


def extract_color_features(image_rgb, image_hsv):
    """
    Mengekstraksi fitur warna RGB dan HSV.

    Menghasilkan:
    - Mean RGB
    - Standard Deviation RGB
    - Mean HSV
    - Standard Deviation HSV
    """

    features = {}

    # =========================
    # EKSTRAKSI FITUR RGB
    # =========================

    rgb_channels = ["R", "G", "B"]

    for i, channel in enumerate(rgb_channels):

        channel_data = image_rgb[:, :, i]

        features[f"mean_{channel}"] = np.mean(channel_data)

        features[f"std_{channel}"] = np.std(channel_data)

    # =========================
    # EKSTRAKSI FITUR HSV
    # =========================

    hsv_channels = ["H", "S", "V"]

    for i, channel in enumerate(hsv_channels):

        channel_data = image_hsv[:, :, i]

        features[f"mean_{channel}"] = np.mean(channel_data)

        features[f"std_{channel}"] = np.std(channel_data)

    return features
