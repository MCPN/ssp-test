import pytest

from src.overlap import calculate_overlap

overlap_data = [
    ('', '', 0),
    ('a', 'b', 0),
    ('a', 'a', 1),
    ('ab', 'bc', 1),
    ('bc', 'ab', 0),
    ('abcd', 'abcd', 4),
    ('aaaabaa', 'aaaaaaa', 2)
]


@pytest.mark.parametrize('s1,s2,expected', overlap_data)
def test_overlap(s1, s2, expected):
    assert calculate_overlap(s1, s2) == expected
