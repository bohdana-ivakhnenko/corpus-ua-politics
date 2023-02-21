import pytest
from processing.analyses import Analysis

name_politician = "zelenskyi"
politician = Analysis(name_politician, data_directory='../testing/data/')

_test_cases_rule = [
    ["old", "expected result for old data"],
    ["new", "expected result for new data"]
]

@pytest.mark.parametrize("test_case", _test_cases_rule)
def test_some_rule(test_case):
    # use data to get the result of analysis from your rule
    politician.rule(test_case[0])
    assert politician.rule_result[test_case[0]] == test_case[1]  # (expected result)


_test_cases_rule_freq = [
    ["old", 0.26],
    ["new", 1.0]
]


@pytest.mark.parametrize("test_case", _test_cases_rule_freq)
def test_rule_freq(test_case):
    politician.rule_freq(test_case[0])
    assert politician.rule_freq_result[test_case[0]] == test_case[1]


if __name__ == '__main__':
    test_some_rule()
    test_rule_freq()
