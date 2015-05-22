def inject_headers(headers, mime):
    for key in headers:
        del mime[key]
        mime[key] = headers[key]
