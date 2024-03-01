### Bug Analysis
The bug occurs in the `request_httprepr` function when trying to concatenate the HTTP Host header. The error message indicates that the `parsed.hostname` variable is `NoneType`, causing the `to_bytes` function to throw a `TypeError` since it expects a string or bytes object.

### Bug Fix Strategy
The `parsed.hostname` variable being `None` suggests that the URL parsed does not have a hostname, which can happen for non-HTTP URLs like `file://`. To fix this bug, we need to handle cases where `parsed.hostname` is `None` and provide a default value.

### Corrected Version of the Function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    host = parsed.hostname if parsed.hostname else b""
    
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(host) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    
    return s
```

This corrected version handles cases where `parsed.hostname` is `None` by providing an empty bytes object as the default value for the `host` variable. This change ensures that the `to_bytes` function does not encounter a `TypeError` when converting the `host` value.