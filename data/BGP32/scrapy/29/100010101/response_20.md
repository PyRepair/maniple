### Bug Explanation
The bug in the `request_httprepr` function occurs when the `parsed.hostname` is `None`. In the failing test case, the input URL `"file:///tmp/foo.txt"` does not contain a hostname, resulting in `parsed.hostname` being `None`. This causes an issue when trying to concatenate `parsed.hostname` to a byte string in the line `s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"`, since the function `to_bytes` cannot handle `None` values.

### Bug Fix Strategy
To fix the bug, we need to handle the case where `parsed.hostname` is `None` before attempting to convert it to bytes. One way to do this is to check if `parsed.hostname` is not `None` before concatenating it to the byte string. If it is `None`, we can provide a default value. 

### Corrected Function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.hostname:  # Check if hostname is not None
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    else:
        s += b"Host: localhost\r\n"  # Default hostname if None
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    return s
```

The corrected function now includes a check for `parsed.hostname` to handle the case where it might be `None`. If `parsed.hostname` is not `None`, it will be concatenated to the byte string; otherwise, a default hostname of "localhost" is used. This fix should address the bug and ensure that the function handles the scenario where the hostname is missing.