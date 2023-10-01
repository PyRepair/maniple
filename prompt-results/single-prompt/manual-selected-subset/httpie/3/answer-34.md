The error message indicates that when attempting to decode the `value` variable, it is `None` and thus the decode operation fails. A simple fix would be to check if the `value` variable is `None` before attempting to decode.

Here is the fixed version of `update_headers` method:

```python
def update_headers(self, request_headers):
    """
    Update the session headers with the request ones while ignoring
    certain name prefixes.

    :type request_headers: dict

    """
    for name, value in request_headers.items():
        if value is None:
            continue
        value = value.decode('utf8')
        if name == 'User-Agent' and value.startswith('HTTPie/'):
            continue

        for prefix in SESSION_IGNORED_HEADER_PREFIXES:
            if name.lower().startswith(prefix.lower()):
                break
            else:
                self['headers'][name] = value
```

This version checks if a `value` is`None` before attempting to decode it, thus preventing the AttributeError. Since it is only adding an extra check, it is unlikely to affect other already passed tests.