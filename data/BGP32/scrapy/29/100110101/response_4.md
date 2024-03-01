### Analysis
The error occurs when parsing a non-HTTP URL because the `parsed.hostname` is `None` in this case, causing the `to_bytes` function to raise a `TypeError` since it expects a string. The `parsed.hostname` remains `None` due to the URL not having a valid hostname. To fix this, we need to handle the case where `parsed.hostname` is `None` by providing a default value or condition.

### Bug Fix Strategy
- Check if `parsed.hostname` is `None` and handle this case by providing a default value.
- Update the construction of the `Host` header to accommodate non-HTTP URLs.

### Corrected Version
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
  
    host = to_bytes(parsed.hostname) if parsed.hostname else b""
    host = host + b"\r\n" if host else b""
  
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + host
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
``` 

This corrected version includes handling the `None` case for `parsed.hostname` by providing a default value of an empty byte string. It also adjusts the construction of the `Host` header to suit non-HTTP URLs. This fixes the issue with non-HTTP URLs causing a `TypeError`.