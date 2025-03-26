import os
import tempfile

import audio_steganogra
import image_steganogra
from data import DATA_DIR


def test_hide_audio():
    file = str(DATA_DIR / "short.mp3")
    secret_message = "# embed_message_image(filename[0], hide_me"

    with tempfile.TemporaryDirectory() as temp_dir:
        out_path = os.path.join(temp_dir, "stego_audio.mp3")
        audio_steganogra.embed_message(file, secret_message, out_path)
        assert secret_message == audio_steganogra.extract_message(out_path)


def test_hide_image():
    file = str(DATA_DIR / "cat.jpg")
    secret_message = "# embed_message_image(filename[0], hide_me, filename[1])"

    with tempfile.TemporaryDirectory() as temp_dir:
        out_path = os.path.join(temp_dir, "stego_image.jpg")
        image_steganogra.embed_message(file, secret_message, out_path)
        assert secret_message == image_steganogra.extract_message(out_path)
