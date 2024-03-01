## Analysis
The buggy function `request_httprepr` is meant to return the raw HTTP representation of a given request. The bug seems to be related to how the `parsed.hostname` is used when constructing the output bytes `s`.

## Bug Explanation
The bug occurs because the `hostname` attribute in the `parsed` object is not directly related to the `host` entry in the raw HTTP representation. This causes incorrect output when constructing the `s` bytes with the hostname.

## Bug Fix
To fix the bug, we should directly use the `parsed.netloc` attribute instead of trying to extract the `hostname`. Furthermore, we need to distinguish between the absence of a port and the presence of a port in the `netloc` to construct the `Host` header correctly.

## Corrected Function
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    
    netloc = parsed.netloc
    if ":" in netloc:
        host, port = netloc.split(":", 1)
        host_bytes = to_bytes(host)
        port_bytes = to_bytes(port)
    else:
        host_bytes = to_bytes(netloc)
        port_bytes = b""
    
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + host_bytes
    if port_bytes:
        s += b":" + port_bytes
    s += b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
``` 

By using the corrected function, the expected values and types of variables for both provided cases will be satisfied.