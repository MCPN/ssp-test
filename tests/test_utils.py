from collections import Counter

import pytest

from utils import ensure_substring_free

test_data = [
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


@pytest.mark.parametrize('strings,expected', test_data)
def test_ensure_substring_free(strings, expected):
    free = ensure_substring_free(strings)
    assert len(free) == len(expected) and not list(Counter(free) - Counter(expected))
