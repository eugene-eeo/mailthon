import mimetypes


def guess(filename, fallback='application/octet-stream'):
    guessed, encoding = mimetypes.guess_type(filename, strict=False)
    if guessed is None:
        return fallback, encoding
    return guessed, encoding
