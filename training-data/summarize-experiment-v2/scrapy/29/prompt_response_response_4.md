The issue in the `request_httprepr` function is that when using the `urlparse_cached` function, the `hostname` attribute of the parsed result is `None` for non-HTTP URLs. This causes an error when trying to concatenate `b"Host: "` with `to_bytes(parsed.hostname)`.

To fix this issue, we can check if the scheme of the URL is "http" before trying to access the `parsed.hostname` attribute. If the scheme is not "http", we can use the `netloc` attribute instead.

Here's the corrected code for the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    if parsed.scheme == 'http':
        host = to_bytes(parsed.hostname)
    else:
        host = to_bytes(parsed.netloc.split(":")[0])
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + host + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this correction, the function should now handle non-HTTP URLs properly and pass the failing test.