import mimetypes


def inject_headers(headers, mime):
    for key in headers:
        del mime[key]
        mime[key] = headers[key]


def guess(filename, fallback):
    guessed, encoding = mimetypes.guess_type(filename, strict=False)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding
