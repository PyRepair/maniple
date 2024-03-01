### Analysis:
The error message indicates that the `to_bytes` function is receiving a `NoneType` object instead of the expected `unicode`, `str`, or `bytes` object. This is likely due to the `parsed.hostname` being `None`.

### Bug Location:
The bug is located in the line where `parsed.hostname` is used to construct the `Host` header line in the HTTP request.

### Cause of the Bug:
The bug is caused by `parsed.hostname` being potentially `None` when parsing a non-HTTP request (like "file:///tmp/foo.txt"). The `parsed.hostname` should be checked for `None` before trying to convert it to bytes.

### Strategy for Fixing the Bug:
To fix the bug, we need to check if `parsed.hostname` is `None`, and if it is, handle this case gracefully without trying to convert it to bytes.

### Corrected Version of the Function:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + (to_bytes(parsed.hostname) if parsed.hostname is not None else b"") + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

### Explanation:
The corrected version of the function checks if `parsed.hostname` is not `None` before converting it to bytes. If it is `None`, an empty byte string is used instead to ensure that the `to_bytes` function receives a valid input. This modification ensures that the function can handle non-HTTP requests gracefully without raising a `TypeError`.