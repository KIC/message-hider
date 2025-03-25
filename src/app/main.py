import os

import audio_steganogra
import click
from key import extract_key_from_gif_deterministic


@click.group()
def cli():
    pass


@cli.group()
def key():
    pass


@cli.group()
def audio():
    pass


@cli.group()
def image():
    pass


@key.command()
@click.option("-s", "--seed", default="42", type=str)
@click.option("-l", "--length", default=32, type=int)
@click.option("-p", "--pixel-entropy", default=100, type=int)
@click.argument("filename", nargs=1)
def generate(seed: str, length: int, pixel_entropy: int, filename: str):
    print(extract_key_from_gif_deterministic(filename, seed, pixel_entropy, length))


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
