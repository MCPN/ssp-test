from typing import List


def ensure_substring_free(strings: List[str]) -> List[str]:
    """
    Remove strings that are substrings of some other strings in the given list
    """
    strings = list(set(strings))
    substrings = set()
    for i in range(len(strings)):
        for j in range(len(strings)):
            if i == j:
                continue
            if strings[i] in strings[j]:
                substrings.add(i)

    return [string for i, string in enumerate(strings) if i not in substrings]
