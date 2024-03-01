### Bug Analysis:
The bug in the `request_httprepr` function lies in how the `parsed.hostname` value is being used in the function. In the case of non-HTTP requests like FTP or file, the `parsed.hostname` should not be used as the `Host` header value since it might not always be present or meaningful. This leads to incorrect HTTP representation for non-HTTP requests.

### Strategy for Fixing the Bug:
1. Check the scheme of the URL to determine if it's an HTTP URL or something else.
2. If the scheme is not HTTP, avoid using `parsed.hostname` as the `Host` header value.
3. Update the function to generate the correct HTTP representation for non-HTTP requests.

### Corrected Version of the Function:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.scheme == 'http':
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    
    s += b"\r\n"
    s += request.body
    return s
``` 

By updating the function to consider the scheme of the URL, the corrected version will now correctly handle non-HTTP requests like FTP or file, preventing the misuse of `parsed.hostname` in creating the `Host` header value. This will ensure that the function generates the correct HTTP representation for all types of requests.