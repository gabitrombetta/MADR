import re


def sanitize(string):
    sanitized_string = re.sub(r'[^a-zA-Z\s]', '', string)
    sanitized_string = sanitized_string.lower()
    sanitized_string = ' '.join(sanitized_string.split())

    return sanitized_string
