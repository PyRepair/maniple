## Analysis:
The `request_httprepr` function is failing when receiving a non-HTTP request (e.g., "file://", "ftp://") because of the `parsed.hostname` being `None` in those cases. This results in the `to_bytes` function receiving a `None` value, which raises a `TypeError` since it expects a string or bytes object.

## Bug Cause:
The bug occurs because the `parsed` object from `urlparse_cached(request)` does not have a `hostname` attribute when the URL scheme is not HTTP. This results in `parsed.hostname` being `None`, causing the `TypeError` in the `to_bytes` function.

## Fix Strategy:
To fix the bug, we need to handle the case where `parsed.hostname` is `None`. We can modify the code to check if `parsed.hostname` is `None` and provide a default value or handle it differently.

## Corrected Version:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    if parsed.hostname:
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this corrected version, the function now checks if `parsed.hostname` is not `None` before trying to convert it to bytes. This modification will prevent the `TypeError` when dealing with non-HTTP URLs.