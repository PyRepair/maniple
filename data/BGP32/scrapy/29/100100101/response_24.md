The bug in the `request_httprepr` function lies in the incorrect handling of the `parsed.hostname` value when generating the raw HTTP representation. The function is using `parsed.hostname` directly, which is empty for non-HTTP requests, instead of utilizing `parsed.netloc` which contains the hostname for all schemes.

To fix this bug, we need to update the code to use `parsed.netloc` instead of `parsed.hostname` in the line where the Host header is constructed.

Here is the corrected version of the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.netloc) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this correction, the `request_httprepr` function should now handle non-HTTP requests correctly and produce the expected output for the failing test cases provided.