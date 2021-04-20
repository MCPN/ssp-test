import pytest
from networkx import symmetric_difference

from src import HierarchicalGraph

trivial_data = [
    (
        [
            'abc',
            'bcd',
            'cde',
        ],
        5,
    ),
    (
        [
            'cde',
            'bcd',
            'abc',
        ],
        9,
    ),
    (
        [
            'abcde',
            'dedef',
            'fabc',
        ],
        11,
    )
]


@pytest.mark.parametrize('strings,expected', trivial_data)
def test_trivial_solution(strings, expected):
    hg = HierarchicalGraph(strings)
    hg.construct_trivial_graph()
    result = hg.to_string()
    assert len(result) == expected

    for string in strings:
        assert string in result


greedy_data = [
    (
        [
            'abc',
            'bcd',
            'cde',
        ],
        5,
    ),
    (
        [
            'cde',
            'bcd',
            'abc',
        ],
        5,
    ),
    (
        [
            'abcde',
            'dedef',
            'fabc',
        ],
        9,
    ),
    (
        [
            'GTCCC',
            'TGCCA',
            'CCCGA',
            'ATGCC',
            'CCGAA',
        ],
        13,
    ),
]


@pytest.mark.parametrize('strings,expected', greedy_data)
def test_greedy_solution(strings, expected):
    hg = HierarchicalGraph(strings)
    hg.construct_greedy_graph()
    result = hg.to_string()
    assert len(result) == expected

    for string in strings:
        assert string in result


deterministic_data = [
    (
        [
            'ccaeae',
            'eaeaea',
            'aeaecc',
        ],
        'eaeaeaccaeaecc',
    ),
    (
        [
            'ccaeae',
            'aeaecc',
            'eaeaea',
        ],
        'eaeaeaccaeaecc',
    ),
]


@pytest.mark.parametrize('strings,expected', deterministic_data)
def test_gha_is_deterministic_to_order(strings, expected):
    hg = HierarchicalGraph(strings)
    hg.construct_greedy_graph()
    assert hg.to_string() == expected


collapsing_data = [
    [
        'abc',
        'bcd',
        'cde',
    ],
    [
        'cde',
        'bcd',
        'abc',
    ],
    [
        'abcde',
        'dedef',
        'fabc',
    ],
    [
        'GAA',
        'TGG',
        'GGA',
    ],
]


@pytest.mark.parametrize('strings', collapsing_data)
def test_collapsed_greedy_solution(strings):
    hg = HierarchicalGraph(strings)
    hg.construct_greedy_graph()
    graph = hg.graph.copy()

    # CA(GHA) == GHA
    hg.double_and_collapse()
    assert len(symmetric_difference(hg.graph, graph).edges()) == 0
