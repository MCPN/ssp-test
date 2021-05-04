from collections import Counter

import pytest

from utils import counting_sort, ensure_substring_free

ensure_substring_free_data = [
    (
        [
            'abc',
            'bcd',
            'cde',
        ],
        [
            'abc',
            'bcd',
            'cde',
        ],
    ),
    (
        [
            'abc',
            'bc',
            'cde',
        ],
        [
            'abc',
            'cde',
        ],
    ),
    (
        [
            'a',
            'b',
            'b',
            'c',
            'c',
            'b',
        ],
        [
            'a',
            'b',
            'c',
        ],
    ),
]


@pytest.mark.parametrize('strings,expected', ensure_substring_free_data)
def test_ensure_substring_free(strings, expected):
    free = ensure_substring_free(strings)
    assert len(free) == len(expected) and not list(Counter(free) - Counter(expected))


counting_sort_data = [
    (
        [
            (1, 1),
            (2, 2),
            (3, 3),
        ],
        {
            (1, 1): 3,
            (2, 2): 2,
            (3, 3): 1,
        },
        [
            (1, 1),
            (2, 2),
            (3, 3),
        ],
    ),
(
        [
            (1, 1),
            (2, 2),
            (3, 3),
        ],
        {
            (1, 1): 4,
            (2, 2): 2,
            (3, 3): 2,
        },
        [
            (1, 1),
            (2, 2),
            (3, 3),
        ],
    ),
]


@pytest.mark.parametrize('element,reference,expected', counting_sort_data)
def test_counting_sort(element, reference, expected):
    assert counting_sort(element, reference) == expected
