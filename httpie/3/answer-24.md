To fix the bug in this code snippet, we can add a conditional statement to check if the `value` is `None` before trying to decode it. Here's the modified version of the `update_headers` function:

```python
def update_headers(self, request_headers):
    """
    Update the session headers with the request ones while ignoring
    certain name prefixes.

    :type request_headers: dict

    """
    for name, value in request_headers.items():
        if value is not None:
            value = value.decode('utf8')
        if name == 'User-Agent' and value.startswith('HTTPie/'):
            continue

        for prefix in SESSION_IGNORED_HEADER_PREFIXES:
            if name.lower().startswith(prefix.lower()):
                break
            else:
                self['headers'][name] = value
```

By checking if `value` is not `None`, we can avoid the AttributeError. This change should fix the problem and pass the `tests/test_sessions.py::TestSession::test_download_in_session` test without affecting other tests.