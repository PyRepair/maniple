### Analysis
The error message indicates a `TypeError` in the function `to_bytes`. The cause of the bug seems to be that the `parsed.hostname` value is `None`, leading to the `TypeError` of trying to convert a `NoneType` to bytes.

### Bug Explanation
The bug occurs because the `urlparse_cached` function returns a `ParseResult` object, where the `hostname` attribute is `None` in cases where the scheme is not `http` or `https`. As a result, when trying to concatenate the host in the `s` variable, the `to_bytes` function encounters a `NoneType` instead of a string.

### Bug Fix
To fix the bug, we should check if the `parsed.hostname` is `None` before concatenating it with the `s` variable. We can set the hostname to an empty string if it is `None`, ensuring that the `to_bytes` function receives a valid string input.

### Corrected Function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)

    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    host = to_bytes(parsed.hostname) if parsed.hostname else b""
    
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + host + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body

    return s
```

By handling the `None` case for `parsed.hostname`, we can avoid the `TypeError` and ensure that the function works correctly in scenarios where the scheme is not `http` or `https`. This fix should pass the failing test cases and provide the expected output values.