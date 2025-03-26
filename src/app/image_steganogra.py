import tempfile

from utils import run_binary


def embed_message(image_path, message, output_path):
    with tempfile.NamedTemporaryFile("w") as temp_file:
        temp_file.write(str(message))
        temp_file.flush()

        std, err = run_binary("jsteg", "hide", image_path, temp_file.name, output_path)
        if err:
            raise ValueError(f"\n{std}\n{err}")


def extract_message(stego_image_path):
    std, err = run_binary("jsteg", "reveal", stego_image_path)
    if err:
        raise ValueError(f"\n{std}\n{err}")

    return std
