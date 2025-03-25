from data import DATA_DIR
from key import extract_key_from_gif_deterministic


def test_deterministic():
    assert extract_key_from_gif_deterministic(
        DATA_DIR / "mrbean.gif", 42.42
    ) == extract_key_from_gif_deterministic(DATA_DIR / "mrbean.gif", 42.42)
    assert extract_key_from_gif_deterministic(
        DATA_DIR / "mrbean.gif", 42.42
    ) != extract_key_from_gif_deterministic(DATA_DIR / "mrbean.gif", 42.41)
