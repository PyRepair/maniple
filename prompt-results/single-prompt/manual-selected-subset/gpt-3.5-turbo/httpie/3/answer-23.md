Here is the fixed version of the update_headers function:

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
        
        if name == 'User-Agent' and (value is None or value.startswith('HTTPie/')):
            continue

        skip = False
        for prefix in SESSION_IGNORED_HEADER_PREFIXES:
            if name.lower().startswith(prefix.lower()):
                skip = True
                break
        if not skip:
            self['headers'][name] = value
```

The changes include checking if the value is None before attempting to decode it, and also adding a condition to ignore the header if the value is None for the User-Agent case. Additionally, a `skip` variable is introduced to control the loop execution for SESSION_IGNORED_HEADER_PREFIXES, allowing the self['headers'][name] = value assignment to be outside the loop.