from twitter_utilities.utilities import find_text, _language, find_n_replace_code, text_to_tweets, submitted_by
import pytest


@pytest.mark.parametrize(
    ["text", "pattern", "result"], [
        ("String", "r", "r"),
        ("String with `x` sample code", ".*`(.*)`.*", "x"),
        ("""With multiple lines of code
        ```r
        x
        ```
        End of line""", "(?<=```)(.*?)(?=```)", """r
        x
        """)
    ]
)
def test_find_text(text, pattern, result):
    matches = find_text(text, pattern)
    for match in matches:
        assert match == result, "test failed"


@pytest.mark.parametrize(
    ["code", "language"],
    [
        ("""python
        x = 1""", "python"),
        ("""  r
        x = 1
        ```""", "r")
    ]
)
def test_language(code, language):
    assert _language(code) == language


def test_language_exception():
    code = """
    no code string"""
    with pytest.raises(ValueError) as e:
        _language(code)
    assert str(e.value) == "Language type not found"


test1 = (
    """In R what would be the output of following?
    ```r
    x = 1
    type(x)
    ```""",
    ["r"],
    ["""x = 1
    type(x)"""],
    """In R what would be the output of following?
 [see_image:1]"""
)

test2 = (
    """In python what would be the output of following?
    ```   python
    x = 1
    type(x)
    python
    ```Additional String""",
    ["python"],
    ["""x = 1
    type(x)
    python"""],
    """In python what would be the output of following?
 [see_image:1] Additional String"""
)

test3 = (
    """In R, which of the following code example would throw an error
    ``` r
    x = 1
    ```
    ``` r
    y = 1
    ```""",
    ["r", "r"],
    ["x = 1", "y = 1"],
    """In R, which of the following code example would throw an error
 [see_image:1] 
 [see_image:2]"""
)

test4 = (
    """In python which of the following would throw an error?
    ```python
    x = 1
    ```
    option 2
    ```python
    x = 2
    ```
    option 3
    ```   python
    x=4
    ```Adding some more boilerplate text to exceed the test limit of 280. All the above three examples would not throw an error when they are run in python""",
    ["python", "python", "python"],
    ["x = 1", "x = 2", "x=4"],

    """In python which of the following would throw an error?
 [see_image:1] 
 option 2
 [see_image:2] 
 option 3
     [see_image:3] Adding some more boilerplate text to exceed the test limit of 280. All the above three examples would not throw an error when they are run in python""",
)

test5 = (
    """This is a string without code text. In today's tweetorial we will talk about There are two things to note here. First: Indexing with `NA`, and Second: Indexing with logicals. When you index with `NA`, you get `NA`. When you index with logical vectors, the positions with `TRUE` gets selected and the ones with `FALSE` are dropped. If in case your logical vector is of smaller length, its elements are recycled to match the corresponding length. So in the above example: `y` is of length 4, so when used as `x[y]`, `y` gets recycled to `(T, F, F, NA, T, F)` and `x` is indexed as `x[c(T, F, F, NA, T, F)]`. Since position 1 and 5 are `TRUE`, those will be returned, the ones with `FALSE` will not be returned and the position which has `NA` will return `NA`. So the output will be `1 NA 5`.""",
    [],
    [],
    """This is a string without code text. In today's tweetorial we will talk about There are two things to note here. First: Indexing with `NA`, and Second: Indexing with logicals. When you index with `NA`, you get `NA`. When you index with logical vectors, the positions with `TRUE` gets selected and the ones with `FALSE` are dropped. If in case your logical vector is of smaller length, its elements are recycled to match the corresponding length. So in the above example: `y` is of length 4, so when used as `x[y]`, `y` gets recycled to `(T, F, F, NA, T, F)` and `x` is indexed as `x[c(T, F, F, NA, T, F)]`. Since position 1 and 5 are `TRUE`, those will be returned, the ones with `FALSE` will not be returned and the position which has `NA` will return `NA`. So the output will be `1 NA 5`."""
)


@pytest.mark.parametrize(
    ["text", "code_language", "code_text", "modified_text"],
    [
        test1,
        test2,
        test3,
        test4,
        test5
    ]
)
def test_find_n_replace_code(text, code_language, code_text, modified_text):
    result = find_n_replace_code(text)
    result_text = result['text']
    result_code_info = result['code_info']

    assert result_text == modified_text

    counter = len(result_code_info)
    if result_code_info:
        for i in range(counter):
            assert f'[see_image:{i+1}]' in result_text

            assert result_code_info[i]['language'] == code_language[i]
            assert result_code_info[i]['code_text'] == code_text[i]
            assert result_code_info[i]['sno'] == i + 1
    else:
        assert len(result_code_info) == 0


@pytest.mark.parametrize(
    ["text"],
    [
        [test1[0]],
        [test2[0]],
        [test3[0]],
        [test4[0]]
    ]
)
def test_text_to_tweets(text):
    tweets = text_to_tweets(text)

    for tweet in tweets:
        assert len(tweet) <= 280


@pytest.mark.parametrize(
    ["name"],
    [
        ["data_question"]
    ]
)
def test_submitted_by(name):
    assert name in submitted_by(name)
