from typing import Dict, List


class DSU:
    """
    Disjoint set union class with additional field for such string that:
    1. It is the shortest among all the strings in set
    2. It is the largest among all the string from step 1
    """
    def __init__(self, strings: List[str]):
        self.last: Dict[str, str] = {string: string for string in strings}
        self._parent: Dict[str, str] = {string: string for string in strings}
        self._rank: Dict[str, int] = {string: 0 for string in strings}

    def find_parent(self, a: str):
        if self._parent[a] != a:
            self._parent[a] = self.find_parent(self._parent[a])
        return self._parent[a]

    def union(self, a: str, b: str):
        a = self.find_parent(a)
        b = self.find_parent(b)
        if a == b:
            return

        if self._rank[a] < self._rank[b]:
            a, b = b, a
        self._parent[b] = a
        if self._rank[a] == self._rank[b]:
            self._rank[a] += 1
        if (-len(self.last[a]), self.last[a]) < (-len(self.last[b]), self.last[b]):
            self.last[a] = self.last[b]
        else:
            self.last[b] = self.last[a]
