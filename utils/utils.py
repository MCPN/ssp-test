from typing import Dict, Iterable, List, Tuple


def counting_sort(elements: Iterable[Tuple[int, int]], keys: Dict[Tuple[int, int], int]):
    """
    Counting sorts elements in reversed order by using keys as a reference
    """
    mx = max(keys.values())
    order = [[] for _ in range(mx + 1)]
    for elem in elements:
        order[mx - keys[elem]].append(elem)
    return [elem for lst in order for elem in lst]


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
