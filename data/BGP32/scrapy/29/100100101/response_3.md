The bug in the `request_httprepr` function is that it's trying to access the `hostname` attribute directly from the parsed URL, which is not available for non-HTTP URLs like `file://` and `ftp://`. This causes the function to fail for non-HTTP requests.

To fix this bug, we need to check if the parsed URL contains a `hostname` attribute before trying to access it. For non-HTTP URLs, we should handle the `hostname` differently.

Here is the corrected version of the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    if parsed.hostname:
        host_header = b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    else:
        host_header = b""
        
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += host_header
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

This corrected version of the function now checks if the `hostname` attribute is available in the parsed URL and sets the `Host` HTTP header accordingly. This fix ensures that the function can handle non-HTTP URLs correctly.

With this fix, the function should now pass the failing test for non-HTTP requests.