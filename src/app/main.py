import base64
import os
from pathlib import Path

import audio_steganogra
import click
from encrypt import decrypt_with_key, encrypt_with_key
from key import (
    extract_key_from_gif_deterministic,
    generate_deterministic_key,
    generate_key_from_jpeg,
    get_random_string_from_book,
)
from seed import generate_secure_random_float, generate_secure_random_integer


@click.group()
def cli():
    pass


@cli.group()
def crypto():
    pass


@cli.group()
def audio():
    pass


@cli.group()
def image():
    pass


@crypto.command()
@click.option("-t", "--type", type=click.Choice(["int", "float"], case_sensitive=False))
@click.option("-l", "--lower", type=int, default=14)
@click.option("-u", "--upper", type=int, default=100000)
def generate_seed(type: str, lower: float, upper: float):
    if type == "int":
        print(generate_secure_random_integer(lower, upper))
    elif type == "float":
        print(generate_secure_random_float(lower, upper))
    else:
        raise ValueError("Invalid seed type.")


@crypto.command()
@click.option("-s", "--seed", default="42", type=str)
@click.option("-l", "--length", default=32, type=int)
@click.option("-p", "--pixel-entropy", default=100, type=int)
@click.argument("filename", nargs=1)
def generate_key(seed: str, length: int, pixel_entropy: int, filename: str):
    if filename.endswith(".gif"):
        print(extract_key_from_gif_deterministic(filename, seed, pixel_entropy, length))
    elif filename.lower().endswith((".jpg", ".jpeg")):
        print(generate_key_from_jpeg(filename, seed, pixel_entropy, length))
    else:
        print(
            generate_deterministic_key(Path(filename).read_text().strip(), seed, length)
        )


@crypto.command()
@click.option("-s", "--seed", default="42", type=str)
@click.option("-p", "--pages", default=120, type=int)
@click.option("-w", "--words", default=250, type=int)
@click.option("-c", "--chars", default=5, type=int)
@click.option("-l", "--length", default=42, type=int)
def generate_source(seed: str, pages: int, words: int, chars: int, length: int):
    for t in get_random_string_from_book(seed, pages, words, chars, length):
        print(t)


@crypto.command()
@click.option("--base64", "base", is_flag=True, default=False)
@click.option("-k", "--key", type=str)
@click.option("-m", "--message", prompt=True, hide_input=True)
def encrypt(key: str, message: str, base: bool):
    message = encrypt_with_key(message, key)
    if base:
        message = base64.b64encode(message)

    print(message)


@crypto.command()
@click.option("--base64", "base", is_flag=True, default=False)
@click.option("-k", "--key", type=str)
@click.option("-m", "--message", prompt=True, hide_input=True)
def decrypt(key: str, message: str, base: bool):
    if base:
        message = base64.b64decode(message)

    print(decrypt_with_key(message, key))


@audio.command()
@click.option(
    "-o", "--out-dir", default="/tmp", type=click.Path(exists=True, file_okay=False)
)
@click.option("--hide-me", prompt=True, hide_input=True, envvar="__HIDE_ME__")
@click.argument("filename", nargs=1)  # -1)
def hide(out_dir: str, target: str, hide_me: str, filename: str):
    print(f"'{hide_me}' '{filename}' '{out_dir}'")
    audio_steganogra.embed_message(
        filename, hide_me, os.path.join(out_dir, os.path.basename(filename))
    )


@audio.command()
@click.argument("filename", nargs=1)  # -1)
def reveil(filename: str):
    print(audio_steganogra.extract_message(filename))


if __name__ == "__main__":
    cli()


if __name__ == "__main__":
    cli()
