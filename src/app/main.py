import base64
import os

import audio_steganogra
import click
from encrypt import decrypt_with_key, encrypt_with_key
from key import extract_key_from_gif_deterministic
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
    print(extract_key_from_gif_deterministic(filename, seed, pixel_entropy, length))


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
