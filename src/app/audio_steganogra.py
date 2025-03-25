import soundfile as sf


def embed_message(audio_path, message, output_path):
    """Embed a secret message into a FLAC file using LSB steganography."""
    audio_data, sample_rate = sf.read(audio_path)

    # Convert the message to binary
    binary_message = "".join(format(ord(char), "08b") for char in message)
    binary_message += "00000000"  # Null terminator

    if len(binary_message) > audio_data.size:
        raise ValueError("Message is too long to embed in the audio file.")

    # Flatten the audio data if it's multi-channel
    flattened_audio = audio_data.flatten()

    # Embed the message
    for i in range(len(binary_message)):
        sample = flattened_audio[i]
        sample_as_int = int(sample * (2**15))
        sample_as_int = (sample_as_int & ~1) | int(binary_message[i])
        flattened_audio[i] = sample_as_int / (2**15)

    # Reshape the audio data back to its original shape
    embedded_audio = flattened_audio.reshape(audio_data.shape)

    sf.write(output_path, embedded_audio, sample_rate, format="FLAC")
    print(f"Message embedded and saved as {output_path}")


def extract_message(stego_audio_path):
    """Extract a secret message from a FLAC file using LSB steganography."""
    audio_data, _ = sf.read(stego_audio_path)

    # Flatten the audio data if it's multi-channel
    flattened_audio = audio_data.flatten()

    binary_message = ""
    for sample in flattened_audio:
        sample_as_int = int(sample * (2**15))
        binary_message += str(sample_as_int & 1)

        if len(binary_message) % 8 == 0:
            if binary_message[-8:] == "00000000":
                break

    message = ""
    for i in range(0, len(binary_message) - 8, 8):
        char = chr(int(binary_message[i : i + 8], 2))
        if char == "\0":
            break
        message += char
    return message
