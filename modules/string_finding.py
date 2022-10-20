"""Deals with finding strings inside strings, and substituting those strings"""""


def find_occurrences(text: str, find: str, block: bool = False, match_case: bool = False, word_only: bool = False) -> list[int]:
    """Finds all occurrences the substring sub inside 'text'. Returns the first indexes of the occurrences.

    Arguments:
        block - If two occurrences overlap, only the first is considered, creating "blocky" occurrences.
        match_case - The case of 'find' is considered.
        word_only - The 'find' will try to find exact spacing matches; e.g., "he is" is not in "I know he isn't ok", but
            it is in "I know he is".
    """
    if len(find) == 0:
        return []

    first_indexes: list[int] = []

    if not match_case:
        text = text.upper()
        find = find.upper()

    # Finding

    if word_only:
        word_list: list[str] = text.split(" ")
        find_word_list: list[str] = find.split(" ")

        first_word_index: int = 0
        last_possible_index: int = len(word_list) - len(find_word_list)
        while first_word_index <= last_possible_index:
            punctuation: set = {"\n", "!", "?", ",", "."}

            # Calculating the subtext
            punctuation_in_find: bool = False
            for char in find:
                if char in punctuation:
                    punctuation_in_find = True
                    break

            if punctuation_in_find:
                sub_text = word_list[first_word_index: first_word_index + len(find_word_list)]
            else:
                sub_text = word_list[first_word_index: first_word_index + len(find_word_list) - 1]

                last_sub_text: str = ""
                for char in word_list[first_word_index + len(find_word_list) - 1]:
                    if char in punctuation:
                        break
                    last_sub_text += char

                if last_sub_text != "":
                    sub_text.append(last_sub_text)

            # Calculating whether found
            if find_word_list == sub_text:
                text_index: int = len("".join(word_list[:first_word_index])) + first_word_index
                first_indexes.append(text_index)

                first_word_index += (len(find_word_list) - 1) * block

            first_word_index += 1

        return first_indexes


    last_possible_index: int = len(text) - len(find)
    first_char_index: int = 0
    while first_char_index <= last_possible_index:
        sub_text = text[first_char_index: first_char_index + len(find)]

        if sub_text == find:
            first_indexes.append(first_char_index)
            first_char_index += (len(find) - 1) * block

        first_char_index += 1

    return first_indexes


def substitute(text: str, replacing: str, replacement: str, match_case: bool = True, word_only: bool = False):
    list_indexes: list[int] = find_occurrences(text, replacing, block=True, match_case=match_case, word_only=word_only)
    list_indexes.reverse()

    for first_index in list_indexes:
        last_index: int = first_index + (len(replacing) - 1)
        text = text[:first_index] + replacement + text[last_index + 1:]

    return text
