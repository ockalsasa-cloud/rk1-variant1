import pytest

from main import chunk


@pytest.mark.parametrize(
    "items, size, expected",
    [
        ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3], 10, [[1, 2, 3]]),
        ([], 2, []),
    ],
)
def test_chunk(items: list[int], size: int, expected: list[list[int]]) -> None:
    assert chunk(items, size) == expected
