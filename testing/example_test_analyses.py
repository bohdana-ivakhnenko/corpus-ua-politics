import pytest
from processing.analyses import Analysis

_test_cases_rule = [
    "expected result 1",
    "expected result 2"
]

name_politician = ""
politician = Analysis(name_politician)


@pytest.mark.parametrize("test_case", _test_cases_rule)
def test_some_rule(test_case):
    # use data to get the result of analysis from your rule
    politician.rule()
    assert politician.rule_result == test_case  # (expected result)


if __name__ == '__main__':
    test_some_rule()
