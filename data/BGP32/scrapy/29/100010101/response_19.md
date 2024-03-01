### Bug Analysis
The bug occurs because the `parsed` object does not necessarily have a `hostname` attribute when the URL scheme is not `http` or `https`. This causes the `parsed.hostname` to be `None`, leading to a `NoneType` error when trying to concatenate with a byte string in the line `s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"`.

### Bug Fix Strategy
To fix this bug, we need to handle the case where `parsed.hostname` is `None` by providing a default value for the `Host` header. We can use the `netloc` attribute from the parsed URL as the hostname if `parsed.hostname` is `None`.

### Corrected Function
```python
from six.moves.urllib.parse import urlunparse
from scrapy.utils.python import to_bytes
from scrapy.utils.httpobj import urlparse_cached

def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    hostname = parsed.hostname if parsed.hostname else parsed.netloc
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

After applying this correction, the function should be able to handle URLs with schemes other than `http` or `https` properly, and the provided test case should pass without any errors.