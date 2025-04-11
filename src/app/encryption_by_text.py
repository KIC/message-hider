import re
import secrets
from typing import Iterator

import fitz

# TODO:
#  add text staganbography i.e.
#
# - very fancy ML based steganography https://github.com/mickeysjm/StegaText/blob/master/run_single_end2end.py
# - whitespace stego based on java https://darkside.com.au/snow/
# - using typos as stego based on nodejs https://github.com/mjethani/typo
#


def get_text(file: str) -> list[list[list[str]]]:
    def extract_text(page: fitz.Page, num: int) -> list[str]:
        # Detect column boundaries (ignore footer and text over images)
        # bboxes = column_boxes(page, footer_margin=50, no_image_text=True)

        # Extract text from each column
        # from multi_column import column_boxes
        #   Download utility: https://github.com/pymupdf/PyMuPDF-Utilities
        # columns_text = [page.get_text(clip=rect, sort=True) for rect in bboxes]
        #
        # for i, text in enumerate(columns_text):
        #     print(f"Column {i + 1}:\n{text}\n")
        return [[re.split(r"\s+", l) for l in re.split(r"\n|\r\n|\r", page.get_text())]]

    doc = fitz.open(str(file))
    return [extract_text(page, num) for num, page in enumerate(doc)]


def _find_word(
    search: str, text: list[list[list[str]]]
) -> tuple[int, int, int, int, int] | None:
    search = search.strip()
    assert search, "Can not searh for empty word"
    found = []

    for page_num, page in enumerate(text):
        for column_num, column in enumerate(page):
            for line_num, line in enumerate(column):
                for word_num, word in enumerate(line):
                    if search in word:
                        found.append(
                            (
                                page_num + 1,
                                column_num + 1,
                                line_num + 1,
                                word_num + 1,
                                word.index(search) + 1,
                                len(search),
                            )
                        )

    if not found:
        return None

    return secrets.choice(found)


def find_word(
    search: str, text: list[list[list[str]]]
) -> list[tuple[int, int, int, int, int]]:
    search_words = [search]
    found = []

    while search_words:
        search_word = search_words.pop(0)
        res = None

        for i in range(len(search_word)):
            res = _find_word(search_word[:-i] if i > 0 else search_word, text)
            if res:
                if i > 0:
                    search_words.append(search_word[-i:])
                found.append(res)
                break

        if not res:
            raise ValueError(
                f"'{search_word[: -i + 1]}' of '{search}' could not be found!"
            )

    return found


def gen_key_for_text(
    search: str, text: list[list[list[str]]]
) -> Iterator[tuple[int, int, int, int, int]]:
    words = re.split(r"\s+", search)
    for word in words:
        yield find_word(word, text)


def gen_key_for_pdf(search: str, file: str) -> Iterator[tuple[int, int, int, int, int]]:
    text = get_text(file)
    words = re.split(r"\s+", search)
    for word in words:
        yield find_word(word, text)
