### Bug Analysis
The error message indicates that the `parsed.hostname` is `None` which leads to the `TypeError` in the `to_bytes` function. This occurs because the function `urlparse_cached` does not populate the `hostname` attribute properly for non-HTTP URLs.

### Bug Fix Strategy
We need to handle the case where the `hostname` attribute is `None` and provide a default value in the `s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"` line. We can check if `parsed.hostname` is `None` and set it to an empty string in such cases.

### Corrected Function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    # Fix the bug by checking the hostname attribute
    hostname = parsed.hostname if parsed.hostname else ''
    
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(hostname) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    
    return s
```

Now, the corrected function should handle the case where `parsed.hostname` is `None` and set it to an empty string before encoding it to bytes. This fix should pass the failing test cases provided in the bug description.