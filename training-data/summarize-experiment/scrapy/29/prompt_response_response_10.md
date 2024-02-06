The error occurs at the line `s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"` in the `request_httprepr` function. This is because the `parsed.hostname` can be `None` for non-HTTP URLs, but the `to_bytes` function does not handle `None` values and raises a TypeError.

To fix the bug, we need to handle the case where `parsed.hostname` is `None` and provide a default value. We can use the `netloc` attribute of the `parsed` variable, which contains the network location part of the URL.

Here's the corrected code for the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))

    if parsed.hostname:
        host = to_bytes(parsed.hostname)
    else:
        host = to_bytes(parsed.netloc)

    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + host + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

This revised version of the function checks if `parsed.hostname` is `None`, and if so, it uses `parsed.netloc` as the host. This should resolve the issue of the function throwing a TypeError for non-HTTP URLs.