import base64


def encrypt_sentence():
    pass


def create_key(word1: str, word2: str) -> str:
    b1, b2 = word1.encode(), word2.encode()
    max_len = max(len(b1), len(b2))
    b1_padded = b1.ljust(max_len, b"\x00")
    b2_padded = b2.ljust(max_len, b"\x00")
    xor_key = bytes(a ^ b for a, b in zip(b1_padded, b2_padded))
    return f"{len(b2)}:{base64.b64encode(xor_key).decode()}"


def recover_word(word1: str, key: str) -> str:
    length_str, b64_xor = key.split(":")
    length = int(length_str)
    xor_key = base64.b64decode(b64_xor)
    b1_padded = word1.encode().ljust(len(xor_key), b"\x00")
    b2 = bytes(a ^ b for a, b in zip(b1_padded, xor_key))[:length]
    return b2.decode()
