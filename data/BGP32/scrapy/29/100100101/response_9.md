### Explanation:
The bug in the original function `request_httprepr` is that it assumes every URL passed to it is an HTTP request, which is not the case. The function tries to construct an HTTP representation even for non-HTTP requests, leading to incorrect representations and potentially causing issues.

### Strategy for fixing the bug:
To fix the bug, the function needs to handle non-HTTP requests properly by checking the scheme of the URL before constructing the HTTP representation. If the scheme is not 'http' or 'https', the function should handle the request appropriately based on that scheme.

### The corrected version of the function:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    if parsed.scheme not in ['http', 'https']:
        return to_bytes(request.method) + b" " + to_bytes(request.url) + b" HTTP/1.1\r\n"
    
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

This corrected version of the function first checks if the scheme of the URL is 'http' or 'https'. If it's not, it constructs a basic representation for non-HTTP requests. Otherwise, it proceeds as before for HTTP requests.

By making this change, the function will now handle non-HTTP requests appropriately without causing unexpected behavior.