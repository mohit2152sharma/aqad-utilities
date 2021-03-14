import re
from datetime import datetime


def find_text(text: str, pattern: str) -> str:
    """
    Given a text text and pattern it finds the pattern matches from the text
    Args:
        text: text text
        pattern: pattern to search for
    Returns:
        A list of matches
    """
    return re.findall(pattern, text, flags=re.S)


def _language(code: str) -> str:
    """
    finds the language tag from code
    Args:
        code: code text
    Returns:
        language
    """
    try:
        language = re.search("^ *\w+?\n", code, re.S).group(0).strip()
    except:
        raise ValueError("Language type not found")

    return language


def find_n_replace_code(text: str, pattern: str = "(?<=```)(.*?)(?=```)", replacement: str = "see_image") -> str:
    """
    In a text, finds code text and replaces it with the given replacement.
    Args:
        text: 
            text in which code is to be replaced
        pattern: 
            pattern used to search for code text. Defaults to "(?<=```)(.*?)(?=```)".
            Assumes the code is between ```.
        replacement:
            replacement text for replacing code matches. If matches are there, replacement text also includes
            a counter.
    Returns:
        A dictionary with replaced text and code information.
        {
            "text": original_replaced_text [see_image_1],
            "code_info": [{
                "language": programming_language,
                "code_text": code_text,
                'sno': sno
            }]
        }
    """

    code_matches = find_text(text, pattern)

    counter = 1
    code_info = []

    for i in range(0, len(code_matches), 2):
        text = text.replace(code_matches[i], f"[{replacement}:{counter}]")

        language = _language(code_matches[i])
        sanitize_code = re.sub(language, "", code_matches[i], 1).strip()

        code_info.append(
            {
                "language": language,
                "code_text": sanitize_code,
                "sno": counter
            }
        )
        counter += 1

    text = text.replace("```", " ")
    text = re.sub(" +", " ", text, re.S)

    return {
        "text": text.strip(),
        "code_info": code_info
    }


def text_to_tweets(text: str, hashtags: list = None):
    """
    converts a text string into tweets, by making sure the text is within character limit
    Args:
        text: for tweets
        hashtags: Any hashtags to append to the string. Defaults to None
    Returns:
        A list of tweets
    """

    str_to_append = ""
    if hashtags is not None:
        for hashtag in hashtags:
            str_to_append += "#" + hashtag + " "

    timestamp = datetime.now().strftime("%d%m%Y%H%M%S")
    str_to_append += f"[TimeStamp:{timestamp}]"

    threshold = 280 - len(str_to_append) - 1

    words = text.split(" ")

    tweets = [""]
    for word in words:
        text = tweets[-1]
        if len(" ".join([text, word])) <= threshold:
            tweets[-1] = " ".join([text, word])
        else:
            tweets.append(word)

    tweets_list = []
    for tweet in tweets:
        t = tweet + " " + str_to_append
        tweets_list.append(t.strip())

    return tweets_list


def submitted_by(name: str) -> str:
    """
    Args:
        name: the twitter handle
    Returns:
        a string with twitter handle appened
    """
    return f"The tweet was submitted by @{name}"