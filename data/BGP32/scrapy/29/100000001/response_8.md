The bug in the provided function `request_httprepr` is caused by concatenating byte strings and a non-byte string (`request.body`) without ensuring that `request.body` is converted to a byte string. This can lead to a `TypeError` when trying to concatenate byte and non-byte strings.

Here's a strategy to fix the bug:
1. Ensure that the `request.body` is properly converted to a byte string before concatenating it with other byte strings.

Here's the corrected version of the function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    
    if request.body is not None:
        s += to_bytes(request.body)

    return s
```

In this corrected version, I added a check to ensure that `request.body` is not `None` before converting it to a byte string and appending it to the `s` byte string.

This fix ensures that the function works correctly without raising a `TypeError` when concatenating byte and non-byte strings.