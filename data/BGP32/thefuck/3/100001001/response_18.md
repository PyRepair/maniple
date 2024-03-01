### Bug Explanation
The bug in the provided function lies in how it reads the output from the `Popen` process. The `proc.stdout.read()` method returns a `bytes` object, not a `str` object directly, and this leads to issues when trying to decode it using `decode('utf-8')`.

### Bug Fix
To fix this bug, we need to properly handle the decoding of the output from `Popen` and convert it to a `str` object before using it. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    version = version_bytes.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By first storing the output of `proc.stdout.read()` in `version_bytes` and then decoding it to a `str` object, the decoding issue should be resolved. This corrected version should now properly return the expected shell name and version.