### Analysis
The error message indicates that the `parsed.hostname` value is `None` in the function `request_httprepr` while it is trying to convert it to bytes. This leads to a `TypeError` in the `to_bytes` function because it expects a valid `str` value.

### Bug Explanation
The bug occurs because the `urlparse_cached` function returns a `ParseResult` object where sometimes the `hostname` attribute can be `None`, especially for non-HTTP URLs like `file://` or `ftp://`. When this `None` value is accessed in the `request_httprepr` function, it results in a `NoneType` being passed to the `to_bytes` function, causing the `TypeError` to be raised.

### Bug Fix Strategy
To fix the bug, we need to handle the case where `parsed.hostname` can be `None` and provide a default value or handle it accordingly to prevent the `TypeError`. We can modify the function to check if `parsed.hostname` is `None` before converting it to bytes.

### Corrected Function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    host = b""
    if parsed.hostname:
        host = b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    s += host
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    
    return s
```

By adding the check for `parsed.hostname` before converting it to bytes, the corrected function will handle the `None` case appropriately, and the function should now pass the failing test cases with the expected input/output values.