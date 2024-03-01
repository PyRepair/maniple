### Explanation:
The error occurs because the `parsed.hostname` can be `None` when using a non-HTTP URL scheme like `file://` or `ftp://`. In those cases, the `parsed` object does not have a `hostname` attribute, leading to a `NoneType` error when trying to concatenate `b"Host: " + to_bytes(parsed.hostname) + b"\r\n"`.

### Strategy for fixing the bug:
We need to handle the case where `parsed.hostname` is `None` for non-HTTP URL schemes. We can modify the code to first check if `parsed.hostname` is `None` before trying to concatenate it. If it is `None`, we can provide a default value (e.g., an empty string).

### The corrected version of the function:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.hostname is not None:
        host_header = b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    else:
        host_header = b"Host: \r\n"
    s += host_header
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    
    return s
``` 

This corrected version checks if `parsed.hostname` is not `None` before adding it to the `s` variable. If it is `None`, the function adds a default host header value. This change ensures that the function can handle non-HTTP URL schemes without raising an error.