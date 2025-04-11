from data import DATA_DIR
from encryption_by_text import find_word, get_text


def test_words_in_txt():
    # find words by the longest
    text = get_text(DATA_DIR / "lorum-ipsum.pdf")
    test_words = "found finger aunt belt toe industrial father".split(" ")

    # i would only need one huge string and know for each character which
    #  page, column, and word it was

    # optionally allow substr like: first four letters of each word
    # find all whole words ignoring space

    # for word in test_words:
    for tw in test_words:
        res = find_word(tw, text)
        assert tw == "".join(
            [
                text[p - 1][c - 1][l - 1][w - 1][b - 1 : b + e - 1]
                for p, c, l, w, b, e in res
            ]
        )
