import re


# ** Function to extract regex patterns from given string **

def extract_regex(string, doc, og_string):
    a = []
    expression = string
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        l = [og_string[start:end], start, end]
        a.append(l)
    return a
