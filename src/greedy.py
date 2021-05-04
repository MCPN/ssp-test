from collections import defaultdict
from itertools import permutations
from typing import Dict, List, Iterable, Tuple

import networkx as nx

from .overlap import calculate_overlap
from utils import counting_sort


class GreedySolver:
    def __init__(self, strings: List[str]):
        self._str_to_int: Dict[str, int] = {}
        self._strings: List[str] = strings
        self._overlaps: Dict[Tuple[int, int], int] = {}
        self._n: int = len(strings)

        for i, string in enumerate(strings):
            self._str_to_int[string] = i
        for i, j in permutations(range(self._n), 2):
            self._overlaps[(i, j)] = calculate_overlap(strings[i], strings[j])

    def _path_to_string(self, path: Iterable[Tuple[int, int]]) -> str:
        """
        Converts a path from the overlap graph into string
        :param path: path from the overlap graph
        :return: merged string
        """

        result, start = "", None
        for edge in path:
            if edge[0] >= self._n or edge[1] >= self._n:  # edge from source or to sink
                continue
            if edge[1] == start:  # the last edge in loop
                return result

            if start is None:  # the first edge in path/loop
                start = edge[0]
                result = self._strings[edge[0]]
            overlap = self._overlaps[edge]
            result += self._strings[edge[1]][overlap:]

        return result

    def greedy(self) -> str:
        """
        Solves given SSP instance by using the classical greedy algorithm
        """
        # this case would break path-to-string because the path would be source -> string -> sink
        if len(self._strings) == 1:
            return self._strings[0]

        graph = nx.DiGraph()
        graph.add_nodes_from(range(self._n + 2))  # all the strings plus a source and a sink
        edges = list(permutations(range(self._n), 2))
        edges = counting_sort(edges, self._overlaps)
        edges.extend([(self._n, i) for i in range(self._n)])  # self._n is a source
        edges.extend([(i, self._n + 1) for i in range(self._n)])  # (self._n + 1) is a sink

        reachable = defaultdict(set)
        for edge in edges:
            if graph.out_degree(edge[0]) != 0 or graph.in_degree(edge[1]) != 0 or edge[0] in reachable[edge[1]]:
                continue
            graph.add_edge(*edge)
            prefix = nx.ancestors(graph, edge[1])
            suffix = nx.descendants(graph, edge[0])
            for v in prefix:
                for u in suffix:
                    reachable[v].add(u)

        return self._path_to_string(nx.eulerian_path(graph))

    def t_greedy(self) -> str:
        """
        Solves given SSP instance by using the TGREEDY algorithm
        """
        graph = nx.DiGraph()
        graph.add_nodes_from(range(self._n))
        edges = list(permutations(range(self._n), 2))
        edges = counting_sort(edges, self._overlaps)

        strings = []
        reachable = defaultdict(set)
        for edge in edges:
            if graph.out_degree(edge[0]) != 0 or graph.in_degree(edge[1]) != 0:
                continue
            graph.add_edge(*edge)

            if edge[0] in reachable[edge[1]]:  # cycle
                cycle_string = self._path_to_string(nx.find_cycle(graph, source=edge[0]))
                strings.append(cycle_string)
            else:
                prefix = nx.ancestors(graph, edge[1])
                suffix = nx.descendants(graph, edge[0])
                for v in prefix:
                    for u in suffix:
                        reachable[v].add(u)

        # unlike in GREEDY, some nodes might left isolated
        strings.extend(map(lambda x: self._strings[x], nx.isolates(graph)))
        return GreedySolver(strings).greedy()
