## Bug Explanation
The bug in the provided function is caused by the `parsed.hostname` being `None` when parsing a non-http request like `file://` or `ftp://`. The `parsed.hostname` is expected to be `None` for non-http requests, which leads to a `TypeError` in the `to_bytes` function since it is trying to convert a `None` object to bytes.

## Fix Strategy
To fix this bug, we need to handle cases where `parsed.hostname` can be `None`. We should check if `parsed.hostname` is `None` before trying to encode it to bytes. In cases where `parsed.hostname` is `None`, we should skip adding it to the byte string.

## The corrected version of the function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    if parsed.hostname:
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
``` 

By including the check `if parsed.hostname:` before trying to encode `parsed.hostname` to bytes, we handle the case where `parsed.hostname` can be `None`, preventing the `TypeError` during byte encoding. This fix will pass the failing test cases and handle non-http requests correctly.