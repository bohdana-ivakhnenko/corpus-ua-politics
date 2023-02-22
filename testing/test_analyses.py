import pytest
from processing.analyses import Analysis

name_politician_1 = "zelenskyi"
politician_1 = Analysis(name_politician_1, data_directory='../testing/data/')

name_politician_2 = "klychko"
politician_2 = Analysis(name_politician_2, data_directory='../testing/data/')

_test_cases_rule = [
    ["old", "expected result for old data"],
    ["new", "expected result for new data"]
]


@pytest.mark.parametrize("test_case", _test_cases_rule)
def test_some_rule(test_case):
    # use data to get the result of analysis from your rule
    politician_1.rule(test_case[0])
    assert politician_1.rule_result[test_case[0]] == test_case[1]  # (expected result)


_test_cases_rule_posts_per_day = [
    ["old", 0.26],
    ["new", 1.0]
]


@pytest.mark.parametrize("test_case", _test_cases_rule_posts_per_day)
def test_rule_posts_per_day(test_case):
    politician_1.rule_posts_per_day(test_case[0])
    assert politician_1.rule_posts_per_day_result[test_case[0]] == test_case[1]


_test_cases_rule_size_sentences = [
    ["old", 1.0],
    ["new", 3.5]
]


@pytest.mark.parametrize("test_case", _test_cases_rule_size_sentences)
def test_rule_size_sentences(test_case):
    politician_2.rule_size(test_case[0])
    assert politician_2.rule_size_result_sentences[test_case[0]] == test_case[1]


_test_cases_rule_size_words = [
    ["old", 47.0],
    ["new", 46.5]
]


@pytest.mark.parametrize("test_case", _test_cases_rule_size_words)
def test_rule_size_words(test_case):
    politician_2.rule_size(test_case[0])
    assert politician_2.rule_size_result_words[test_case[0]] == test_case[1]


if __name__ == '__main__':
    test_some_rule()
    test_rule_posts_per_day()
    test_rule_size_sentences()
    test_rule_size_words()
