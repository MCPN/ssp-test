from typing import List

import networkx as nx

from .dsu import DSU
from .overlap import calculate_overlap


class HierarchicalGraph:
    def __init__(self, strings: List[str]):
        self.graph = nx.MultiDiGraph()
        self._strings: List[str] = strings
        self._n: int = len(strings)

        for string in strings:
            for i in range(len(string)):
                for j in range(i + 1, len(string) + 1):
                    self.graph.add_node(string[i:j])
        self.graph.add_node('')

    def to_string(self) -> str:
        """
        Extract an eulerian solution from current graph.
        Warning: if graph does not contain an eulerian solution,
        the behaviour of this function is undefined
        """
        subgraph = self.graph.subgraph(nx.node_connected_component(self.graph.to_undirected(as_view=True), ''))
        path, result = nx.eulerian_path(subgraph, source=''), ''
        for edge in path:
            if len(edge[0]) < len(edge[1]):
                result += edge[1][-1]

        return result

    def double_and_collapse(self):
        """
        Doubles all the edges in given solution and applies the collapsing algorithm
        Warning #1: if graph does not contain a solution, the behaviour of this function is undefined
        Warning #2: if Collapsing Conjecture doesn't hold, this function might produce incorrect solution
        """
        for edge in list(self.graph.edges()):
            self.graph.add_edge(*edge)

        nodes = list(self.graph.nodes())
        nodes.sort(key=lambda x: (-len(x), x))
        dsu = DSU(nodes)
        nodes.pop()  # remove empty string
        input_nodes = set(self._strings)

        for node in nodes:
            prev = node[:-1]
            suff = node[1:]
            prev_suff = node[1:-1]

            while self.graph.has_edge(prev, node) and self.graph.has_edge(node, suff):
                if self.graph.number_of_edges(prev, node) == 1 and self.graph.number_of_edges(node, suff) == 1:
                    if node in input_nodes:  # don't make input node isolated
                        break
                    node_par = dsu.find_parent(node)
                    if self.graph.degree(node) != 2 and dsu.last[node_par] == node:
                        break

                self.graph.remove_edge(prev, node)
                self.graph.remove_edge(node, suff)
                if len(node) > 1:
                    self.graph.add_edge(prev, prev_suff)
                    self.graph.add_edge(prev_suff, suff)

            if self.graph.has_edge(prev, node):
                dsu.union(prev, node)
            if self.graph.has_edge(node, suff):
                dsu.union(node, suff)

    def construct_trivial_graph(self):
        """
        Constructs a trivial solution by merging input strings
        """
        cur_overlap = 0
        for i in range(self._n):
            cur_string = self._strings[i]
            for j in range(cur_overlap, len(cur_string)):
                self.graph.add_edge(cur_string[:j], cur_string[:j + 1])

            cur_overlap = calculate_overlap(cur_string, self._strings[i + 1]) if i + 1 != len(self._strings) else 0
            for j in range(len(cur_string), cur_overlap, -1):
                self.graph.add_edge(cur_string[-j:], '' if j == 1 else cur_string[-j + 1:])

    def construct_greedy_graph(self):
        """
        Constructs a greedy solution using Greedy Hierarchical Algorithm (GHA)
        """
        nodes = list(self.graph.nodes())
        nodes.sort(key=lambda x: (-len(x), x))
        dsu = DSU(nodes)
        nodes.pop()  # remove empty string

        for string in self._strings:
            self.graph.add_edge(string[:-1], string)
            self.graph.add_edge(string, string[1:])
            dsu.union(string[:-1], string)
            dsu.union(string, string[1:])

        for node in nodes:
            if nx.is_isolate(self.graph, node):
                continue
            indegree = sum(self.graph.number_of_edges(vert, node) for vert in self.graph.predecessors(node)
                           if len(vert) == len(node) + 1)
            outdegree = sum(self.graph.number_of_edges(node, vert) for vert in self.graph.successors(node)
                            if len(vert) == len(node) + 1)

            if indegree > outdegree:
                suff = node[1:]
                for _ in range(indegree - outdegree):
                    self.graph.add_edge(node, suff)
                dsu.union(node, suff)
            elif indegree < outdegree:
                pref = node[:-1]
                for _ in range(outdegree - indegree):
                    self.graph.add_edge(pref, node)
                dsu.union(pref, node)
            else:
                # the last chance to connect eps to node
                node_par = dsu.find_parent(node)
                if dsu.find_parent('') != node_par and dsu.last[node_par] == node:
                    self.graph.add_edge(node[:-1], node)
                    self.graph.add_edge(node, node[1:])
                    dsu.union(node[:-1], node)
                    dsu.union(node, node[1:])


class HierarchicalSolver:
    def __init__(self, strings: List[str]):
        self.hg = HierarchicalGraph(strings)

    def gha(self) -> str:
        """
        Solves given SSP instance by using the GHA algorithm
        """
        self.hg.construct_greedy_graph()
        return self.hg.to_string()

    def trivial_ca(self) -> str:
        """
        Solves given SSP instance by using the CA algorithm for the trivial solution
        """
        self.hg.construct_trivial_graph()
        self.hg.double_and_collapse()
        return self.hg.to_string()
