import pytest
from processing.analyses import Analyses

_test_cases = [
    ("data1", "expected result"),
    ("data2", "expected result")
]


@pytest.mark.parametrize("test_case", _test_cases)
def some_rule(test_case):
    # use data to get the result of analysis from your rule
    result = Analyses.rule(test_case[0])
    assert result == test_case[1]  # (expected result)


if __name__ == '__main__':
    some_rule()
