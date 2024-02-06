The error occurs in the `request_httprepr` function when trying to convert the `parsed.hostname` to bytes using the `to_bytes` function, which results in a `NoneType` error. This happens because `parsed.hostname` is an empty string for non-HTTP requests, and the `to_bytes` function does not handle empty strings gracefully.

To fix the bug, we should modify the `to_bytes` function to handle empty strings and ensure it returns an empty bytes object in this case. We can also modify the `request_httprepr` function to include a condition to check for the presence of `parsed.hostname` before converting it to bytes.

Here's the revised version of the function:

```python
def to_bytes(text, encoding=None, errors='strict'):
    """Return the binary representation of `text`. If `text`
    is already a bytes object, return it as-is."""
    if text is None:
        return b''
    if isinstance(text, bytes):
        return text
    if not isinstance(text, six.string_types):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)

def request_httprepr(request):
    parsed = urlparse_cached(request)
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    s = to_bytes(request.method) + b" " + to_bytes(path) + b" HTTP/1.1\r\n"
    if parsed.hostname:
        s += b"Host: " + to_bytes(parsed.hostname) + b"\r\n"
    if request.headers:
        s += request.headers.to_string() + b"\r\n"
    s += b"\r\n"
    s += request.body
    return s
```

With these changes, the function should now be able to handle non-HTTP requests without raising errors.