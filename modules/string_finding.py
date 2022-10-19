"""Deals with finding strings inside strings, and substituting those strings"""""


def find_string(find: str, text: str) -> list[int]:
    """Finds all exact occurrences the substring sub inside 'text'. Returns the first indexes of the occurrences"""

    first_indexes: list[int] = []

    if len(find) == 0:
        return []

    last_possible_index: int = len(text) - len(find)
    for first_char_index in range(0, last_possible_index + 1):
        sub_text = text[first_char_index: first_char_index + len(find)]

        if sub_text == find:
            first_indexes.append(first_char_index)

    return first_indexes


print(find_string("eu", "eu sou eu, o que é demais!eu"))
