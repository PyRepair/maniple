The bug in the `request_httprepr` function lies in the fact that it assumes all requests are HTTP requests and tries to construct an HTTP representation for any type of request. This causes an issue when non-HTTP requests are passed to the function.

To fix this bug, we can modify the `request_httprepr` function to only handle HTTP requests and return an empty byte string for non-HTTP requests.

Here is the corrected version of the `request_httprepr` function:

```python
from six.moves.urllib.parse import urlunparse
from scrapy.utils.python import to_bytes
from scrapy.http import Headers
from scrapy.utils.request import request_fingerprint

def request_httprepr(request):
    if not request.url.startswith('http'):
        return b""

    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))

    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    
    if request.headers:
        s += Headers(request.headers).to_string() + b"\r\n"
    
    s += b"\r\n"
    
    if request.body:
        s += request.body

    return s
```

Explanation:
1. We added a check at the beginning of the function to verify if the request URL starts with 'http'. If it doesn't, we return an empty byte string immediately.
2. Modified the import statement for `to_bytes` to be directly from `scrapy.utils.python`.
3. Changed `request.headers.to_string()` to `Headers(request.headers).to_string()` to ensure correct handling of headers.
4. Added a check for `request.body` before appending it to the final byte string.

With these changes, the `request_httprepr` function will only process HTTP requests and return the correct HTTP representation, handling non-HTTP requests gracefully.