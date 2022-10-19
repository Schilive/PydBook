# Of Change

class Change:
    """One change of characters between two strings, of insertion or deletion."""

    NEW = 0
    DELETED = 1

    def __init__(self, change_type: NEW | DELETED, index: int, character: str):
        """If the character is new, then 'index' is its index. If the character has been deleted, then 'index' is
        its old index."""

        self.change_type = change_type
        self.index = index
        self.character = character


def get_changes(original: str, changed: str) -> list[Change]:
    """Returns a list of changes from 'original' to 'changed'.
        The calculation is the done in the following manner:
        1. Tries to find the (possibly) deleted character by orderly mapping the character of 'original' on 'changed';
        if a character could not be mapped, then it is considered deleted. For example, if 'original' = "Batman' and
        'changed' = "Bye Bat!', then 'B' shall be considered found at index = 0, then 'a' at index = 5, then, lastly,
        't' at index = 6. The other character shall be considered deleted.
        2. The characters in 'changed' which are not considered 'found' shall be considered new."""

    mapped_indexes: set = set({})  # Indexes of mapped characters of 'original' in 'changed'
    differences: list[Change] = []

    # Finding deleted and kept characters from 'original' in 'changed', that is, mapping 'original' into 'changed'

    start_search_index: int = 0
    for original_index in range(0, len(original)):

        searched_character = original[original_index]
        for j in range(0, len(changed[start_search_index:])):

            character_index = j + start_search_index
            character = changed[character_index]

            if character == searched_character:
                start_search_index = character_index + 1
                mapped_indexes.add(character_index)
                break
        else:
            differences.append(Change(Change.DELETED, original_index, searched_character))

    # Finding new characters in 'changed'

    for index in range(0, len(changed)):
        if index not in mapped_indexes:
            differences.append(Change(Change.NEW, index, changed[index]))

    return differences

# Of changes


def remake_str(changed: str, changes: list[Change]) -> str:
    """Returns how the string 'changed' would have been if the changes in 'changes' had been applied to it."""

    # Filtering
    deletion_indexes: set[int] = set({})
    new_char_changes: list[Change] = []

    for change in changes:
        if change.change_type == Change.NEW:
            deletion_indexes.add(change.index)
        else:
            new_char_changes.append(change)

    # Deletion of new characters

    deletions_made = 0
    ch_index = 0
    while ch_index < len(changed):
        del_index = ch_index + deletions_made
        if del_index in deletion_indexes:

            changed = changed[: ch_index] + changed[ch_index + 1:]
            deletions_made += 1
            deletion_indexes.remove(del_index)
        else:
            ch_index += 1

    # Insertion of deleted characters

    def change_key(_change: Change) -> int: return _change.index

    new_char_changes = sorted(new_char_changes, key=change_key)

    for change in new_char_changes:
        changed = changed[: change.index] + change.character + changed[change.index:]

    return changed


def change_str(original: str, changes: list[Change]) -> str:
    """Applies the changes in 'changes' to 'original'."""

    # Filtering

    deletion_indexes: set[int] = set({})
    new_char_changes: list[Change] = []

    for change in changes:
        if change.change_type == Change.DELETED:
            deletion_indexes.add(change.index)
        else:
            new_char_changes.append(change)

    # Deletion of characters to be deleted

    made_deletions: int = 0
    ch_index = 0
    while ch_index < len(original):
        del_index = ch_index + made_deletions

        if del_index in deletion_indexes:
            original = original[: ch_index] + original[ch_index + 1:]
            made_deletions += 1
        else:
            ch_index += 1

    # Insertion of characters to be inserted

    def change_key(_change: Change): return _change.index

    sorted(new_char_changes, key=change_key)

    for change in new_char_changes:
        original = original[: change.index] + change.character + original[change.index:]

    return original


# Of lists of changes

class ChangesList:
    """It is a linear set of changes with a pointer to the last set of changes. Its linearity makes a tree of changes
    impossible, then, if the last set of changes is not the last set of changes and a new set of changes is added to the
    list, all the sets of changes after the last set of changes shall be deleted."""

    def __init__(self, list_changes: list[list[Change]] = None):
        if not list_changes:
            self.changes: list[list[Change]] = []
        else:
            self.changes: list[list[Change]] = list_changes

        self.last_changes_index = len(self.changes) - 1  # It can be negative (-1), which would mean there are no
        # last changes

    def get_last_change(self) -> list[Change]:
        if self.last_changes_index < len(self.changes):
            return self.changes[self.last_changes_index]

        return []

    def get_next_change(self) -> list[Change]:
        if self.last_changes_index + 1 < len(self.changes):
            return self.changes[self.last_changes_index + 1]

        return []

    def add_changes(self, changes: list[Change]) -> None:
        del self.changes[self.last_changes_index + 1:]  # Deletes all the sets of changes after the last set of changes
        self.changes.append(changes)

        self.last_changes_index += 1

    def rollback_changes(self, times: int = 1) -> None:
        self.last_changes_index = max(self.last_changes_index - times, -1)

    def roll_forward_changes(self, times: int = 1) -> None:
        self.last_changes_index = min(self.last_changes_index + times, len(self.changes) - 1)
