### Analysis
The error occurs in the line `s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"` in the `request_httprepr` function. The error message indicates that the `to_bytes` function is receiving a `NoneType` instead of the expected `unicode`, `str`, or `bytes` object. This happens when the `parsed.hostname` is `None`.

### Bug Explanation
The bug occurs because the `parsed.hostname` is not present when the provided URL scheme is not `http` or `https`, which leads to `None` being passed as an argument to the `to_bytes` function. This causes a `TypeError` in the `to_bytes` function.

### Fix Strategy
We need to handle the case where `parsed.hostname` could be `None` by providing a default value in case it is not available.

### Corrected Version
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    hostname = parsed.hostname if parsed.hostname else ''
    
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(hostname) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    
    return s
```

This correction ensures that if the `parsed.hostname` is `None`, it will default to an empty string to prevent the `TypeError` in the `to_bytes` function.