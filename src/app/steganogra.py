import numpy as np
from PIL import Image
from pydub import AudioSegment
from scipy.fftpack import dct, idct


def embed_message_image(cover_image_path, message, output_path):
    """
    Embed a secret message into an image using DCT-based steganography.
    """
    # Open the cover image
    cover_image = Image.open(cover_image_path).convert("L")  # Convert to grayscale
    cover_array = np.array(cover_image)
    height, width = cover_array.shape

    # Convert the message to binary
    binary_message = "".join(format(ord(char), "08b") for char in message)
    binary_message += "11111111"  # Add a termination sequence (8 bits of 1s)
    message_length = len(binary_message)

    # Embed the message into the DCT coefficients
    bit_index = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            if bit_index >= message_length:
                break

            # Get an 8x8 block
            block = cover_array[i : i + 8, j : j + 8]

            # Apply DCT to the block
            dct_block = dct(dct(block.T, norm="ortho").T, norm="ortho")

            # Modify a middle-frequency coefficient to embed a bit
            if bit_index < message_length:
                bit = int(binary_message[bit_index])
                if bit == 1:
                    dct_block[4, 3] = np.floor(dct_block[4, 3] / 2) * 2 + 1
                else:
                    dct_block[4, 3] = np.floor(dct_block[4, 3] / 2) * 2

                bit_index += 1

            # Apply inverse DCT to get back the modified block
            idct_block = idct(idct(dct_block.T, norm="ortho").T, norm="ortho")
            cover_array[i : i + 8, j : j + 8] = np.round(idct_block)

    # Save the stego-image
    stego_image = Image.fromarray(np.clip(cover_array, 0, 255).astype(np.uint8))
    stego_image.save(output_path)


def extract_message_image(stego_image_path):
    """
    Extract a secret message from an image using DCT-based steganography.
    """
    # Open the stego-image
    stego_image = Image.open(stego_image_path).convert("L")
    stego_array = np.array(stego_image)
    height, width = stego_array.shape

    binary_message = ""
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            # Get an 8x8 block
            block = stego_array[i : i + 8, j : j + 8]

            # Apply DCT to the block
            dct_block = dct(dct(block.T, norm="ortho").T, norm="ortho")

            # Extract the bit from the middle-frequency coefficient
            bit = int(dct_block[4, 3]) % 2
            binary_message += str(bit)

            # Check for termination sequence (8 bits of 1s)
            if binary_message.endswith("11111111"):
                break

        if binary_message.endswith("11111111"):
            break

    # Remove the termination sequence and convert binary to text
    binary_message = binary_message[:-8]
    message = "".join(
        chr(int(binary_message[i : i + 8], 2)) for i in range(0, len(binary_message), 8)
    )

    return message


def embed_message(audio_path, message, output_path):
    """
    Embed a secret message into an MP3 file using LSB steganography.
    """
    # Load the audio file
    audio = AudioSegment.from_file(audio_path, format="mp3")
    samples = np.array(audio.get_array_of_samples())

    # Convert message to binary
    binary_message = "".join(format(ord(char), "08b") for char in message)
    binary_message += "11111111"  # Add termination sequence (8 bits of 1s)

    if len(binary_message) > len(samples):
        raise ValueError("Message is too long to embed in the audio file.")

    # Embed the message into the least significant bits of the samples
    for i in range(len(binary_message)):
        bit = int(binary_message[i])
        samples[i] = (samples[i] & ~1) | bit  # Modify LSB

    # Save the modified audio file
    modified_audio = audio._spawn(samples.tobytes())
    modified_audio.export(output_path, format="mp3")
    print(f"Message embedded and saved as {output_path}")


def extract_message(stego_audio_path):
    """
    Extract a secret message from an MP3 file using LSB steganography.
    """
    # Load the stego-audio file
    audio = AudioSegment.from_file(stego_audio_path, format="mp3")
    samples = np.array(audio.get_array_of_samples())

    # Extract the least significant bits from the samples
    binary_message = ""
    for sample in samples:
        binary_message += str(sample & 1)

        # Check for termination sequence (8 bits of 1s)
        if binary_message.endswith("11111111"):
            break

    # Remove termination sequence and convert binary to text
    binary_message = binary_message[:-8]
    message = "".join(
        chr(int(binary_message[i : i + 8], 2)) for i in range(0, len(binary_message), 8)
    )

    return message


# Example usage
if __name__ == "__main__":
    audio_path = "cover_audio.mp3"  # Path to your input MP3 file
    stego_audio_path = "stego_audio.mp3"  # Path to save the output MP3 file
    secret_message = "This is a secret message!"  # Your secret message

    # Embed the secret message into the MP3 file
    embed_message(audio_path, secret_message, stego_audio_path)

    # Extract the secret message from the stego-audio file
    extracted_message = extract_message(stego_audio_path)
    print(f"Extracted message: {extracted_message}")
