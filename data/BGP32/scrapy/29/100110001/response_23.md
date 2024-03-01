### Analysis:
1. The `request_httprepr` function is failing when receiving a non-HTTP request URL like `file:///` or `ftp://`.
2. The error occurs at line 82 in the `request_httprepr` function where the `parsed.hostname` is None for non-HTTP URLs such as `file:///` or `ftp://`.
3. The error message indicates a `TypeError` in the `to_bytes` function because it's receiving a `NoneType` instead of a string for the hostname.
4. To fix this bug, we need to handle cases where the `parsed.hostname` is None for non-HTTP URLs.
5. We can modify the function to check if the URL scheme is not `http` before trying to access the `parsed.hostname`.

### Updated/Copied version:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"

    if parsed.scheme == 'http':
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"

    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

This updated version checks if the URL scheme is `http` before trying to access `parsed.hostname`. It avoids the TypeError when `parsed.hostname` is None for non-HTTP URLs like `file:///`.