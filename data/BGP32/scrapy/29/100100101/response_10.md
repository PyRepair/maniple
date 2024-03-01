## Explanation:
The bug in the `request_httprepr` function lies in the construction of the `Host` header in the HTTP request. The current implementation only uses the `parsed.hostname` attribute, which is not present for non-HTTP URLs (such as `file://` or `ftp://`). This causes the function to fail when processing non-HTTP requests.

## Fix strategy:
To fix the bug, we need to check if the parsed URL is an HTTP request before constructing the `Host` header. For non-HTTP requests, we should use the `parsed.netloc` attribute instead of `parsed.hostname`.

## The corrected version of the function:
```python
from six.moves.urllib.parse import urlunparse
from scrapy.utils.python import to_bytes, to_native_str
from scrapy.utils.httpobj import urlparse_cached
from scrapy.http.request import Request

def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"

    if parsed.scheme == 'http':
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    else:
        s += b"Host: " + to_bytes(parsed.netloc) + b"\r\n"

    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    return s
```

This corrected version of the function includes a conditional check to distinguish between HTTP and non-HTTP requests when constructing the `Host` header. It now correctly uses `parsed.netloc` for non-HTTP requests like `file://` or `ftp://`, resolving the bug.