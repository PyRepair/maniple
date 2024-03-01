Based on the error message and the expected input/output values, the bug in the current function `request_httprepr` is caused by the `parsed.hostname` being `None` when the scheme of the URL is not `http` or `https`. This results in an error when trying to convert `parsed.hostname` to bytes using the `to_bytes` function.

To fix this bug, we need to handle the case when `parsed.hostname` is `None`. We can do this by checking if `parsed.hostname` is not `None` before trying to concatenate it with other byte strings.

Here is the corrected version of the function:

```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    
    if parsed.hostname is not None:
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
        
    s += b"\r\n"
    s += request.body
    return s
```

By adding the `if parsed.hostname is not None` check, we ensure that we only attempt to convert `parsed.hostname` to bytes if it is not `None`. This fix will prevent the `TypeError` that was occurring when `parsed.hostname` was `None`.

With this corrected version, the function should now pass the failing test cases and return the expected output values for both cases mentioned.