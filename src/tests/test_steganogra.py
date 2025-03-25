import os
import tempfile

import numpy as np
import soundfile as sf
from audio_steganogra import embed_message, extract_message


def generate_random_noise_flac(output_path, duration_seconds=60, sample_rate=44100):
    num_samples = duration_seconds * sample_rate
    audio_data = np.random.uniform(-1, 1, num_samples).astype(np.float32)
    sf.write(output_path, audio_data, sample_rate, format="FLAC")
    print(f"Random noise FLAC generated and saved to {output_path}")


def test_hide_audio():
    with tempfile.TemporaryDirectory() as temp_dir:
        cover_audio_path = os.path.join(temp_dir, "cover_audio.flac")
        stego_audio_path = os.path.join(temp_dir, "stego_audio.flac")
        secret_message = "# embed_message_image(filename[0], hide_me, filename[1])"

        generate_random_noise_flac(cover_audio_path)
        embed_message(cover_audio_path, secret_message, stego_audio_path)
        extracted_message = extract_message(stego_audio_path)

        assert secret_message == extracted_message, (
            f"Expected '{secret_message}', but got '{extracted_message}'"
        )
        print("Test passed successfully!")
        assert secret_message == extracted_message, (
            f"Expected '{secret_message}', but got '{extracted_message}'"
        )
