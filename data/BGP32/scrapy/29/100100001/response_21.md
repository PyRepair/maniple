The bug in the `request_httprepr` function is caused by the `parsed.hostname` attribute being `None` when the URL scheme is not `http` or `https`. This leads to a `TypeError` when trying to convert `None` to bytes in the `s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"` line.

To fix this bug and make the function work for non-HTTP requests, we need to handle the case where `parsed.hostname` is `None`. We can modify the function to use `parsed.netloc` instead, which includes both the hostname and port information.

Here is the corrected version of the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.netloc:
        s += b"Host: " + to_bytes(parsed.netloc) + b"\r\n"
        
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
        
    s += b"\r\n"
    s += request.body
    return s
```

With this modification, the function will now correctly handle non-HTTP requests where `parsed.hostname` might be `None`. The corrected function should pass the failing test provided.