import os
import tempfile

import audio_steganogra
import image_steganogra
import numpy as np
import soundfile as sf
from data import DATA_DIR


def test_hide_audio():
    def generate_random_noise_flac(output_path, duration_seconds=60, sample_rate=44100):
        num_samples = duration_seconds * sample_rate
        audio_data = np.random.uniform(-1, 1, num_samples).astype(np.float32)
        sf.write(output_path, audio_data, sample_rate, format="FLAC")
        print(f"Random noise FLAC generated and saved to {output_path}")

    with tempfile.TemporaryDirectory() as temp_dir:
        cover_audio_path = os.path.join(temp_dir, "cover_audio.flac")
        stego_audio_path = os.path.join(temp_dir, "stego_audio.flac")
        secret_message = "# embed_message_image(filename[0], hide_me, filename[1])"

        generate_random_noise_flac(cover_audio_path)
        audio_steganogra.embed_message(
            cover_audio_path, secret_message, stego_audio_path
        )
        extracted_message = audio_steganogra.extract_message(stego_audio_path)

        assert secret_message == extracted_message, (
            f"Expected '{secret_message}', but got '{extracted_message}'"
        )
        print("Test passed successfully!")
        assert secret_message == extracted_message, (
            f"Expected '{secret_message}', but got '{extracted_message}'"
        )


def test_hide_image():
    file = str(DATA_DIR / "cat.jpg")
    secret_message = "# embed_message_image(filename[0], hide_me, filename[1])"

    with tempfile.TemporaryDirectory() as temp_dir:
        out_path = os.path.join(temp_dir, "stego_image.jpg")
        image_steganogra.embed_message(file, secret_message, out_path)
        assert secret_message == image_steganogra.extract_message(out_path)
