import secrets

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_with_key(plaintext: str, key: str) -> str:
    """
    Encrypts a string using AES-256-GCM with a pre-existing 32-byte key.

    :param plaintext: String to encrypt (UTF-8 encoded)
    :param key: 32-byte encryption key (must be exactly 32 bytes)
    :return: Combined nonce + ciphertext + tag (for storage/transmission)
    """
    if len(key) == 64:
        key = bytes.fromhex(key)
    if len(key) != 32:
        raise ValueError(f"Key must be exactly 32 bytes long {len(key)}")

    # Generate random 12-byte nonce (for GCM)
    nonce = secrets.token_bytes(12)

    # Initialize AES-GCM with the provided key
    aesgcm = AESGCM(key)

    # Encrypt and get ciphertext + authentication tag
    ciphertext = aesgcm.encrypt(
        nonce=nonce, data=plaintext.encode("utf-8"), associated_data=None
    )

    # Combine nonce + ciphertext + tag
    return nonce + ciphertext


def decrypt_with_key(encrypted_data: bytes, key: bytes) -> str:
    """
    Decrypts data encrypted with encrypt_with_key()

    :param encrypted_data: Combined nonce + ciphertext + tag
    :param key: 32-byte encryption key used for encryption
    :return: Decrypted plaintext string
    """
    if len(key) == 64:
        key = bytes.fromhex(key)
    if len(key) != 32:
        raise ValueError("Key must be exactly 32 bytes long")

    # Split components (nonce:12 bytes, ciphertext:remaining bytes)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

    # Initialize AES-GCM
    aesgcm = AESGCM(key)

    # Decrypt and verify integrity
    plaintext = aesgcm.decrypt(nonce=nonce, data=ciphertext, associated_data=None)

    return plaintext.decode("utf-8")
