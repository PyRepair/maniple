## Analysis:
The `request_httprepr` function is failing when receiving a non-HTTP request. The issue seems to be related to the `parsed` object generated from the URL of the request. When the URL is a file or ftp request, the `parsed` object might not have the `hostname` attribute, resulting in `parsed.hostname` being `None`.

## Bug:
The bug occurs when trying to concatenate `b"Host: "` with the result of `to_bytes(parsed.hostname)`, where `parsed.hostname` is `None`. The `to_bytes` function expects a valid text input, but it is receiving `None`, causing a `TypeError`.

## Fix:
To fix the bug, we need to handle the case where `parsed.hostname` is `None`. We can check if `parsed.hostname` is not `None` before trying to concatenate it with other bytes.

## Corrected Version:
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

This corrected version includes a check to ensure that `parsed.hostname` is not `None` before trying to concatenate it with other bytes. This modification should prevent the `TypeError` from occurring when processing non-HTTP requests.