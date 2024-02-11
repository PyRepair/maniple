```python
def request_httprepr(request):
    """Return the raw HTTP representation (as bytes) of the given request.
    This is provided only for reference since it's not the actual stream of
    bytes that will be send when performing the request (that's controlled
    by Twisted).
    """
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    method = to_bytes(request.method)
    host = parsed.hostname.encode('utf-8') if parsed.hostname else b""
    headers = request.headers.to_string() + b"\r\n" if request.headers else b""
    body = request.body if request.body else b""
    s = method + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + host + b"\r\n"
    s += headers
    s += b"\r\n"
    s += body
    return s
```