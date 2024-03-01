The bug in the provided function is that it does not handle the case when the `parsed` object does not have a hostname attribute for schemes like 'file' where `netloc` attribute should be used instead. This causes an AttributeError when trying to access `parsed.hostname`. We can fix this by checking if the scheme is 'file' and using `parsed.netloc` instead.

## Corrected version of the function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    if parsed.scheme == 'file':
        hostname = parsed.netloc
    else:
        hostname = parsed.hostname
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

By checking the scheme and using `parsed.netloc` instead of `parsed.hostname` for 'file' schemes, the corrected function should work as expected for both cases provided.