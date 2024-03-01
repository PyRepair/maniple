The bug in the `request_httprepr` function is due to the incorrect handling of the hostname when generating the raw HTTP representation. This results in an incorrect output for non-HTTP requests with different schemes (such as file or ftp).

The issue lies in the line:
```python
s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
```
Here, `parsed.hostname` is not an accurate way to extract the hostname, especially for non-HTTP schemes.

To fix this issue, we need to modify the code to correctly extract the hostname based on the scheme of the request. For non-HTTP schemes, we can directly use the `netloc` attribute from the parsed URL.

Here is the corrected version of the function:
```python
def request_httprepr(request):
    parsed = urlparse_cached(request)
    if parsed.scheme == 'http' or parsed.scheme == 'https':
        hostname = parsed.hostname
    else:
        hostname = parsed.netloc
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    s += b"Host: " + to_bytes(hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With this correction, the function now correctly handles non-HTTP schemes like `file://` or `ftp://` and extracts the hostname appropriately based on the scheme. This should resolve the bug and make the function generate the expected raw HTTP representation for different types of requests.