import os
import tempfile

from utils import run_binary


def embed_message(image_path, message, output_path):
    # Create temp file with manual deletion control
    with tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
        temp_file.write(str(message))
        temp_filename = temp_file.name  # Get filename before closing

    try:
        # File is now closed - safe for external process access
        std, err = run_binary("jsteg", "hide", image_path, temp_filename, output_path)
        if err:
            raise ValueError(f"\n{std}\n{err}")
    finally:
        # Ensure cleanup even if errors occur
        if os.path.exists(temp_filename):
            try:
                os.unlink(temp_filename)
            except Exception:
                pass


def extract_message(stego_image_path):
    std, err = run_binary("jsteg", "reveal", stego_image_path)
    if err:
        raise ValueError(f"\n{std}\n{err}")

    return std
