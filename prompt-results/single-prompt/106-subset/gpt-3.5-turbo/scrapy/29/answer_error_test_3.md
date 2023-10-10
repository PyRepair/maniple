```python
from urllib.parse import urlparse, urlunparse

def request_httprepr(request):
    """Return the raw HTTP representation (as bytes) of the given request.
    This is provided only for reference since it's not the actual stream of
    bytes that will be send when performing the request (that's controlled
    by Twisted).
    """
    parsed = urlparse(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = (request.method or "").encode() + b" " + path.encode() + b" HTTP/1.1\r\n"
    s += b"Host: " + (parsed.hostname or "").encode() + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

Explanation: 
- The `urlparse_cached` function has been replaced with the `urlparse` function from the `urllib.parse` module. 
- The `to_bytes` function has been removed and replaced with the `encode` method, which converts a string to bytes. 
- None values have been handled by explicitly checking for None using the `or` operator and providing a default value of an empty string.