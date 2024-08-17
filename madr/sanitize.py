def sanitize(string):
    sanitized_string = string.lower()
    sanitized_string = ' '.join(sanitized_string.split())

    return sanitized_string
