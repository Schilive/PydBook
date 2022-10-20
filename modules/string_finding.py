"""Deals with finding strings inside strings, and substituting those strings"""""


def find_occurrences(text: str, find: str, block: bool = False) -> list[int]:
    """Finds all occurrences the substring sub inside 'text'. Returns the first indexes of the occurrences.

    Arguments:
        block - If two occurrences overlap, only the first is considered, creating "blocky" occurrences.
    """

    first_indexes: list[int] = []

    if len(find) == 0:
        return []

    last_possible_index: int = len(text) - len(find)
    first_char_index: int = 0
    while first_char_index < last_possible_index + 1:
        sub_text = text[first_char_index: first_char_index + len(find)]

        if sub_text == find:
            first_indexes.append(first_char_index)
            first_char_index += len(find) * block
            continue

        first_char_index += 1

    return first_indexes


def substitute(text: str, replacing: str, replacement: str):
    list_indexes: list[int] = find_occurrences(text, replacing, block=True)
    list_indexes.reverse()

    for first_index in list_indexes:
        last_index: int = first_index + (len(replacing) - 1)
        text = text[:first_index] + replacement + text[last_index + 1:]

    return text
