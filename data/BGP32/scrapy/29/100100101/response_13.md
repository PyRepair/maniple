The bug in the `request_httprepr` function occurs when constructing the HTTP request string, specifically in the `Host` header generation for non-HTTP requests. In the case of non-HTTP requests like `file://` or `ftp://`, the `parsed.hostname` attribute is not populated correctly, leading to an empty `Host` header in the generated HTTP string.

To fix this bug, we need to handle non-HTTP requests differently by checking the scheme of the URL. If it is not `http` or `https`, we should set the `parsed.hostname` to the `parsed.netloc`.

Here is the corrected version of the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    if parsed.scheme not in ('http', 'https'):
        parsed = parsed._replace(hostname=parsed.hostname or parsed.netloc)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this correction, the `parsed.hostname` attribute is now correctly set to `parsed.netloc` for non-HTTP requests, ensuring the `Host` header is populated correctly in the generated HTTP string. This fix should address the bug and pass the failing test cases provided.