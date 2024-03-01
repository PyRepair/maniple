The bug in the `request_httprepr` function lies in the way the hostname is being extracted from the parsed URL. In the original implementation, `parsed.hostname` is used to get the hostname, but for non-HTTP URLs like `file://` and `ftp://`, `parsed.hostname` may not be set correctly.

To fix this bug, we need to handle non-HTTP URLs differently and extract the hostname from `parsed.netloc` instead of `parsed.hostname`.

Here is the corrected version of the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    
    # Extract hostname from netloc for non-HTTP URLs
    hostname = parsed.hostname or parsed.netloc
    
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this corrected implementation, the function should now correctly extract the hostname from the `netloc` field for non-HTTP URLs, ensuring that the test cases provided will pass successfully.