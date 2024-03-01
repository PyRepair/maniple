Based on the error message and the failing test, the issue lies in the `parsed.hostname` value being `None`, which causes the `to_bytes` function to encounter a `NoneType` when trying to convert it into bytes. This occurs when the URL schemes like `file` or `ftp` do not have a hostname, which is expected behavior in these non-HTTP cases.

To fix this issue, we can modify the code to check if the `parsed.hostname` is not `None` before trying to encode it. If it is `None`, we can default to an empty string to avoid the error.

Here is the corrected version of the function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.hostname is not None:
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
        
    s += b"\r\n"
    s += request.body
    
    return s
```

With this modification, when the hostname is `None`, the "Host:" line will be skipped, preventing the `to_bytes` error. This corrected version should now pass the failing test cases and satisfy the expected input/output values.