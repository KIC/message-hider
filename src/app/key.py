import hashlib
import random

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image


def extract_key_from_gif_deterministic(gif_path, seed, num_pixels=10, key_length=32):
    """
    Extracts a deterministic encryption key from a GIF file by selecting
    random pixels of random frames.

    :param gif_path: Path to the GIF file.
    :param seed: Seed for the random number generator (ensures determinism).
    :param num_pixels: Number of pixels to select for key derivation.
    :param key_length: Length of the encryption key.
    :return: Derived encryption key.
    """
    try:
        gif = Image.open(gif_path)
    except Exception as e:
        raise ValueError(f"Error opening GIF file: {e}")

    # Ensure it's an animated GIF with multiple frames
    if not gif.is_animated:
        raise ValueError("The provided file is not an animated GIF.")

    # Collect pixel data from randomly selected frames and pixels
    random.seed(seed)
    pixel_data = bytearray()
    frame_count = gif.n_frames

    for _ in range(num_pixels):
        # Randomly select a frame
        frame_index = random.randint(0, frame_count - 1)
        gif.seek(frame_index)  # Move to the selected frame

        # Convert frame to RGB mode (to handle palettes or grayscale)
        frame = gif.convert("RGB")
        width, height = frame.size

        # Randomly select a pixel from this frame
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Get the RGB value of the pixel and add it to pixel_data
        r, g, b = frame.getpixel((x, y))
        pixel_data.extend([r, g, b])

    # Derive a secure encryption key using PBKDF2-HMAC-SHA256
    salt = hashlib.sha256(pixel_data).digest()[:16]  # Use hash of pixel data as salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(pixel_data)
    gif.close()

    return key.hex()
