### Bug Explanation
The bug in the `request_httprepr` function is caused by the incorrect handling of the `hostname` when the URL scheme is not 'http'. In the case of 'file' or 'ftp' schemes, the `parsed.hostname` will be empty, leading to incorrect HTTP representation generation.

### Bug Fix Strategy
To fix this bug, we need to check the scheme of the URL before setting the `Host` header in the HTTP representation. If the scheme is 'http', we should use `parsed.hostname`, otherwise, we should use `parsed.netloc`.

### Corrected Function
```python
def request_httprepr(request):
    """Return the raw HTTP representation (as bytes) of the given request.
    This is provided only for reference since it's not the actual stream of
    bytes that will be send when performing the request (that's controlled
    by Twisted).
    """
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.scheme == 'http':
        host = parsed.hostname
    else:
        host = parsed.netloc.split("@")[-1].split(":")[0]  # extract hostname for non-http schemes
    
    s += b"Host: " + to_bytes(host) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    return s
```

After applying this correction, the `request_httprepr` function should now correctly handle non-http schemes and generate the expected HTTP representation for those cases.