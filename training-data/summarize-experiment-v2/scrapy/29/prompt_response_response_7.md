The error is occurring in the `to_bytes` function, which is being used to convert `parsed.hostname` to bytes before concatenating it with other byte strings. The error message indicates that the `parsed.hostname` is of type NoneType, which is causing the error when trying to convert it to bytes.

The cause of the bug is that the `parsed.hostname` is not being properly handled when the URL scheme is not 'http' or 'https'. This is evident from the failing test cases where the URLs have schemes of 'file' and 'ftp'.

To fix the bug, we need to handle the case where the URL scheme is not 'http' or 'https' and set the `parsed.hostname` to an empty string in those cases.

Here's the corrected code for the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    if parsed.hostname:
        host = to_bytes(parsed.hostname)
        s += b"Host: " + host + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this correction, the `parsed.hostname` is only converted to bytes and concatenated if it is not None, which resolves the error. This code should now pass the failing test cases.