The bug in the given function is that it is not handling the case when the scheme of the URL is 'file'. The 'file' scheme does not have a hostname, which leads to an empty hostname in the parsed result, causing an issue when constructing the HTTP representation.

To fix this bug, we need to check if the scheme is 'file' and handle it separately to set the 'Host' header correctly.

Here is the corrected version of the function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    
    if parsed.scheme == 'file':
        host = b''
    else:
        host = b"Host: " + to_bytes(parsed.hostname) + b"\r\n"

    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))

    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += host
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

This corrected version now includes the check for 'file' scheme and sets the 'Host' header to an empty byte string when the scheme is 'file'. This ensures that the HTTP representation is constructed correctly for URLs with the 'file' scheme.