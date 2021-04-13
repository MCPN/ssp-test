import pytest

from src import GreedySolver


path_to_string_data = [
    (  # just a path
        [
            'abc',
            'bcd',
            'cde',
            'def',
        ],
        [
            (0, 1),
            (1, 2),
            (2, 3),
        ],
        'abcdef'
    ),
    (  # cycle
        [
            'abc',
            'bcd',
            'cde',
            'def',
        ],
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
        ],
        'abcdef'
    ),
    (  # path with attached sink and source
        [
            'abc',
            'bcd',
            'cde',
            'def',
        ],
        [
            (4, 0),
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 5),
        ],
        'abcdef'
    ),
]


@pytest.mark.parametrize('strings,path,expected', path_to_string_data)
def test_path_to_string(strings, path, expected):
    gs = GreedySolver(strings)
    assert gs._path_to_string(path) == expected


greedy_data = [
    (
        [
            'cde',
            'bcd',
            'ab',
        ],
        'abcde',
    ),
    (
        [
            'a',
            'b',
            'c',
        ],
        'abc',
    ),
    (
        ['abc'],
        'abc',
    ),
]


@pytest.mark.parametrize('strings,expected', greedy_data)
def test_greedy(strings, expected):
    gs = GreedySolver(strings)
    assert gs.greedy() == expected


t_greedy_data = [
    (
        [
            'ab',
            'bc',
            'ca',
            'de',
            'ef',
            'fd',
        ],
        8,
    ),
    (
        [
            'a',
            'b',
            'c',
        ],
        3,
    ),
]


@pytest.mark.parametrize('strings,expected', t_greedy_data)
def test_t_greedy(strings, expected):
    gs = GreedySolver(strings)
    res = gs.t_greedy()
    assert len(res) == expected
    for string in strings:
        assert string in res
