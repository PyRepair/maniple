### Analysis:
1. The `request_httprepr` function takes a `Request` object and constructs a raw HTTP representation as bytes for the request. It extracts necessary information from the request object like method, headers, body, and constructs the HTTP request line.
2. In the buggy function, the parsing of the URL from the request object and constructing the HTTP representation seems to be correct.
3. The bug lies in the construction of the Host header when the scheme is not 'http' or 'https', which leads to the failing test cases for non-HTTP requests like 'file://' and 'ftp://'.
4. To fix the bug, we need to handle cases where the scheme is not 'http' or 'https' and construct the Host header appropriately.

### Bug Explanation:
When the scheme of the URL in the request is not 'http' or 'https', the `parsed.hostname` is empty, leading to an incorrect Host header in the raw HTTP representation. This causes the failing test cases for non-HTTP requests.

### Bug Fix Strategy:
1. Update the code to handle cases where the scheme is not 'http' or 'https'.
2. Extract the netloc value from the parsed URL and use it in the Host header construction.
3. Ensure that the Host header is correctly formatted for non-HTTP requests.

### Corrected Version of the Function:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    if parsed.scheme in ('http', 'https'):
        host_header = b"Host: " + to_bytes(parsed.hostname)
    else:
        host_header = b"Host: " + to_bytes(parsed.netloc)
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += host_header + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this correction, the function now handles non-HTTP requests correctly by constructing the Host header based on the parsed netloc value. This fix should make the failing test cases for non-HTTP requests pass.