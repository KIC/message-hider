import hashlib
import random
from typing import Iterable

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from PIL import Image
from pydub import AudioSegment


def extract_key_from_gif_deterministic(gif_path, seed, num_pixels=100, key_length=32):
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


def generate_key_from_jpeg(
    jpeg_path, seed, num_pixels: int = 100, length: int = 32
) -> str:
    """
    Generates a 32-byte encryption key from a JPEG file using a deterministic
    random selection process.

    :param jpeg_path: Path to the JPEG file.
    :param seed: Seed for the random number generator (ensures determinism).
    :param num_pixels: Number of pixels to select for key derivation.
    :return: Derived 32-byte encryption key.
    """
    try:
        img = Image.open(jpeg_path)
    except Exception as e:
        raise ValueError(f"Error opening JPEG file: {e}")

    # Ensure it's a valid image
    if not img.mode == "RGB":
        img = img.convert("RGB")

    # Initialize random generator with the given seed for determinism
    random.seed(seed)

    # Collect pixel data from randomly selected pixels
    pixel_data = bytearray()
    width, height = img.size

    for _ in range(num_pixels):
        # Randomly select a pixel
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)

        # Get the RGB value of the pixel and add it to pixel_data
        r, g, b = img.getpixel((x, y))
        pixel_data.extend([r, g, b])

    # Derive a secure encryption key using PBKDF2-HMAC-SHA256
    salt = hashlib.sha256(pixel_data).digest()[:16]  # Use hash of pixel data as salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(pixel_data)

    return key.hex()


def get_random_string_from_book(
    seed: int, pages: int, words: int = 250, characters: int = 5, length: int = 42
) -> Iterable[tuple[int, int, int]]:
    random.seed(seed)
    for _ in range(length):
        page = random.randint(1, pages)
        word = random.randint(1, words)
        character = random.randint(1, characters)
        yield page, word, character


def generate_deterministic_key(text: str, seed: int, length: int = 32) -> str:
    """
    Generate a deterministic 32-byte encryption key from a given text and seed.

    :param text: The input text to derive the key from.
    :param seed: The seed for deterministic randomness.
    :return: A 32-byte encryption key.
    """
    random.seed(seed)

    # Generate a deterministic salt using the seed
    salt = "".join(
        random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16)
    ).encode()

    # Use PBKDF2-HMAC-SHA256 to derive the key
    key = hashlib.pbkdf2_hmac("sha256", text.encode(), salt, 100_000, dklen=length)

    return key.hex()


def generate_key_from_mp3(mp3_path, seed, num_samples=1000, length: int = 32) -> str:
    """
    Generates a 32-byte encryption key from an MP3 file using a deterministic random selection process.

    :param mp3_path: Path to the MP3 file.
    :param seed: Seed for the random number generator (ensures determinism).
    :param num_samples: Number of audio samples to select for key derivation.
    :return: Derived 32-byte encryption key.
    """
    try:
        audio = AudioSegment.from_mp3(mp3_path)
    except Exception as e:
        raise ValueError(f"Error opening MP3 file: {e}")

    # Convert audio to raw bytes
    raw_audio = audio.raw_data

    # Initialize random generator with the given seed for determinism
    random.seed(seed)

    # Collect audio sample data from randomly selected positions
    sample_data = bytearray()
    audio_length = len(raw_audio)

    for _ in range(num_samples):
        # Randomly select a sample position
        position = random.randint(0, audio_length - 1)

        # Get the byte at the selected position and add it to sample_data
        sample_data.append(raw_audio[position])

    # Derive a secure encryption key using PBKDF2-HMAC-SHA256
    salt = hashlib.sha256(sample_data).digest()[:16]  # Use hash of sample data as salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    key = kdf.derive(sample_data)

    return key.hex()
