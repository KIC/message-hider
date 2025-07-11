## Hider

Small utility to encrypt a message and hide it in a file like an audio, image
or video.

### Usage

1. think of a secret seed which can be any kind of string or generate one from
   the provided commands
1. Optionally: Hide the seed in a file i.e. a flac file
1. Optionally: create a source text file from a book
1. Create an encryption key using the provided commands from a gif or text or
   use any other 32bytes key you already have (in hex -> 64 Characters)
1. Use the generated key to encrypt your secret message
1. Hide the encrypted message in a file i.e. a flac file
1. distribute the encrypted message/file

Now, to restore your message you need to know your key or the seed in oder to
regenerate the key. Then decrypt the message with the key. tada!
Don't forget to regularly check if you can re-generate the key i.e. by using a
different test seed.

### Install

You can download the binary executable for windows (hider.exe), linux (hider)
requires GLIBC >=2.38 and macOS (mc-hider). Alternatively there is a docker
image on github registry and a flatpack app. Of course you can clone the repo
and use your local python.

In any case, make sure you have ffmpeg installed if you plan to use audio
files.

#### Flatpak (Linux)

You can install the Flatpak bundle from the GitHub release page:

1. Download `hider.flatpak` from the [GitHub Releases](https://github.com/KIC/message-hider/releases) page.
2. Install it with:
   ```bash
   flatpak install --user --bundle hider.flatpak
   ```
3. Run the app with:
   ```bash
   flatpak run org.hider.Hider
   ```
