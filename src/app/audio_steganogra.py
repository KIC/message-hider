import os
import tempfile
from pathlib import Path

from mp3stego import Steganography


def embed_message(audio_path, message, output_path):
    """Embed a secret message into a mp3."""
    stego = Steganography(quiet=True)
    stego.hide_message(audio_path, output_path, message)


def extract_message(stego_audio_path):
    """Extract a secret message from a mp3."""
    stego = Steganography(quiet=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        out_file = os.path.join(temp_dir, "message.txt")

        stego.reveal_massage(stego_audio_path, out_file)
        return Path(out_file).read_text()
