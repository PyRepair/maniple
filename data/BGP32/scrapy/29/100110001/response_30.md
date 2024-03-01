### Analysis:
1. The function `request_httprepr` is failing the test case `test_request_httprepr_for_non_http_request` due to a TypeError being raised in the `to_bytes` function call with `parsed.hostname` being `None`.
2. The error occurs because `parsed.hostname` is `None` for non-HTTP requests like `file:///tmp/foo.txt` and `ftp://localhost/tmp/foo.txt`.
3. The bug is caused by assuming `parsed.hostname` will always have a value, causing the `to_bytes` function to raise a TypeError when attempting to convert `None` to bytes.
4. To fix the bug, we need to check if `parsed.hostname` is not `None` before attempting to concatenate it in the string.
5. Below is the corrected version of the `request_httprepr` function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    if parsed.hostname:  # Check if hostname is not None
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
``` 

By adding the check `if parsed.hostname:` before attempting to use `to_bytes(parsed.hostname)`, we prevent the TypeError from occurring when `parsed.hostname` is `None`.