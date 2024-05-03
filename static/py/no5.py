import re

def test_regex(pattern, string):
    string = string.replace('+', '|')
    if re.match(pattern, string):
        if re.match(pattern, string).group(0) != string:
            return True
        else:
            return False
    else:
        return False