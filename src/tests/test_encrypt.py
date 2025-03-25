import secrets

from encrypt import decrypt_with_key, encrypt_with_key


def test_encrypt():
    key = secrets.token_bytes(32)  # Your existing 32-byte key
    message = "Top secret message"

    # Encrypt
    assert decrypt_with_key(encrypt_with_key(message, key), key) == message
