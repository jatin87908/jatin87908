from pathlib import Path

import cv2
import numpy as np
from rembg import remove


ROOT = Path(__file__).resolve().parent.parent

INPUT_IMAGE = ROOT / "source-photo.jpg"
OUTPUT_IMAGE = ROOT / "source-prepped.png"


def main():
    if not INPUT_IMAGE.exists():
        raise FileNotFoundError(
            f"Input image not found: {INPUT_IMAGE}"
        )

    print("Reading image...")
    image = cv2.imread(str(INPUT_IMAGE))

    if image is None:
        raise RuntimeError("Could not read source-photo.jpg")

    print("Removing background...")
    with open(INPUT_IMAGE, "rb") as file:
        input_data = file.read()

    output_data = remove(input_data)

    temp_path = ROOT / "source-no-bg.png"

    with open(temp_path, "wb") as file:
        file.write(output_data)

    print("Loading processed image...")
    image = cv2.imread(str(temp_path), cv2.IMREAD_UNCHANGED)

    if image is None:
        raise RuntimeError("Could not load background-removed image.")

    # Handle RGBA output from rembg
    if image.shape[2] == 4:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]

        # White background
        white = np.full_like(bgr, 255)

        alpha_float = alpha.astype(np.float32) / 255.0
        alpha_float = alpha_float[:, :, None]

        image = (
            bgr.astype(np.float32) * alpha_float
            + white.astype(np.float32) * (1 - alpha_float)
        ).astype(np.uint8)

    print("Converting to grayscale...")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("Enhancing contrast...")
    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Slightly increase contrast
    enhanced = cv2.normalize(
        enhanced,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    cv2.imwrite(str(OUTPUT_IMAGE), enhanced)

    # Remove temporary file
    temp_path.unlink(missing_ok=True)

    print()
    print("Done!")
    print(f"Created: {OUTPUT_IMAGE}")


if __name__ == "__main__":
    main()