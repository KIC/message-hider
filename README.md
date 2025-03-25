ecoys.py

# Required: pip install pycryptodome stegano Pillow

from Crypto.Cipher import AES
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Random import get_random_bytes
from binascii import hexlify, unhexlify
from stegano import lsb
import random
import os
import shutil

# ------------------

# Encryption Module

# ------------------

def encrypt_seed_with_decoys(seed_phrase: bytes, k: int, n: int, total_images: int, image_paths: list) -> None:
"""
Encrypts a seed phrase using Shamir's Secret Sharing and hides it in images.
Adds extra decoy images with bogus data.

    :param seed_phrase: The seed phrase to encrypt (as bytes).
    :param k: Minimum number of shares required to reconstruct the key.
    :param n: Number of valid shares to generate.
    :param total_images: Total number of images (including decoys).
    :param image_paths: List of image file paths to use for embedding.
    """
    if total_images < n:
        raise ValueError("Total images must be greater than or equal to n (number of valid shares).")
    if len(image_paths) < total_images:
        raise ValueError("Not enough image paths provided for total_images.")

    # Generate random AES key
    key = get_random_bytes(32)  # AES-256

    # Split key using Shamir's scheme
    shares = Shamir.split(k, n, key)

    # Setup directories
    shutil.rmtree('shares', ignore_errors=True)
    os.makedirs('shares', exist_ok=True)

    # Embed valid shares into images
    valid_indices = random.sample(range(total_images), n)  # Randomly select indices for valid shares
    valid_shares = {idx: share for idx, share in zip(valid_indices, shares)}

    for idx in range(total_images):
        if idx in valid_shares:
            # Embed a valid share in this image
            share_idx, share_data = valid_shares[idx]
            secret_data = f'{share_idx},{hexlify(share_data).decode()}'
        else:
            # Embed bogus data in this image
            bogus_data = get_random_bytes(32)
            secret_data = f'{random.randint(1, 255)},{hexlify(bogus_data).decode()}'

        # Hide the data in the image using LSB steganography
        secret_image = lsb.hide(image_paths[idx], secret_data)
        secret_image.save(f'shares/share_{idx + 1}.png')

    # Encrypt seed phrase and save it separately in an additional image
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(seed_phrase)
    encrypted_data = hexlify(cipher.nonce + tag + ciphertext).decode()

    last_image_path = image_paths[-1]
    secret_image = lsb.hide(last_image_path, encrypted_data)
    secret_image.save('encrypted_seed.png')

# ------------------

# Decryption Module

# ------------------

def decrypt_seed_with_decoys(valid_indices: list) -> bytes:
"""
Decrypts the seed phrase using valid indices of images containing real shares.

    :param valid_indices: List of indices (1-based) for the valid share images.
    :return: The recovered seed phrase as bytes.
    """
    if len(valid_indices) < 5:
        raise ValueError("At least 5 valid indices are required to reconstruct the key.")

    # Collect valid shares from specified indices
    shares = []
    for idx in valid_indices:
        fname = f'shares/share_{idx}.png'
        secret_data = lsb.reveal(fname)
        share_idx, share = secret_data.split(',')
        shares.append((int(share_idx), unhexlify(share)))

    # Reconstruct key from valid shares
    key = Shamir.combine(shares)

    # Decrypt seed from image
    encrypted_data = unhexlify(lsb.reveal('encrypted_seed.png'))
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    seed = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return seed
    except ValueError:
        raise RuntimeError("Invalid shares or corrupted data")

# --------

# Usage Example

# --------

if **name** == "**main**": # Example usage (5-of-7 scheme with 8 images total)

    # Provide at least 8 images for embedding (7 for shares + 1 for encrypted seed)
    image_paths = [
        'image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg',
        'image5.jpg', 'image6.jpg', 'image7.jpg', 'image8.jpg'
    ]

    # Encrypt with decoys (5-of-7 scheme)
    encrypt_seed_with_decoys(
        b'your_24_word_seed_phrase_here',
        k=5,
        n=7,
        total_images=8,
        image_paths=image_paths
    )

    # Decrypt using correct indices (user must know these!)
    try:
        correct_indices = [1, 3, 4, 6, 7]  # Example of correct indices (1-based)
        recovered_seed = decrypt_seed_with_decoys(correct_indices)
        print(f"Recovered seed: {recovered_seed.decode()}")

    except RuntimeError as e:
        print(f"Error during decryption: {e}")
