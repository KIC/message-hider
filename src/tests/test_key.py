from data import DATA_DIR
from key import (
    extract_key_from_gif_deterministic,
    generate_deterministic_key,
    generate_key_from_jpeg,
    get_random_string_from_book,
)


def test_deterministic_from_gif():
    file = "mrbean.gif"
    assert len(extract_key_from_gif_deterministic(DATA_DIR / file, 12)) == 64
    assert extract_key_from_gif_deterministic(
        DATA_DIR / file, 42.42
    ) == extract_key_from_gif_deterministic(DATA_DIR / file, 42.42)
    assert extract_key_from_gif_deterministic(
        DATA_DIR / file, 42.42
    ) != extract_key_from_gif_deterministic(DATA_DIR / file, 42.41)


def test_deterministic_from_jpeg():
    file = "cat.jpg"
    assert len(generate_key_from_jpeg(DATA_DIR / file, 12)) == 64
    assert generate_key_from_jpeg(DATA_DIR / file, 42.42) == generate_key_from_jpeg(
        DATA_DIR / file, 42.42
    )
    assert generate_key_from_jpeg(DATA_DIR / file, 42.42) != generate_key_from_jpeg(
        DATA_DIR / file, 42.41
    )


def test_deterministic_from_str():
    key = "a8F2zXqL9mNpW7KdR3vT6yJ4bCgQ5xH2sZrY8wMtP"
    assert len(generate_deterministic_key(key, 12)) == 64
    assert generate_deterministic_key(key, 42.42) == generate_deterministic_key(
        key, 42.42
    )
    assert generate_deterministic_key(key, 42.42) != generate_deterministic_key(
        key, 42.41
    )


def test_random_source():
    assert list(get_random_string_from_book(42.42, 100)) == list(
        get_random_string_from_book(42.42, 100)
    )
    assert list(get_random_string_from_book(42.42, 100)) != list(
        get_random_string_from_book(42.41, 100)
    )
