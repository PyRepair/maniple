### Explanation:
The bug in the provided function lies in how the output from `proc.stdout.read()` is being handled. The `read()` method is returning a MagicMock object instead of the actual output string. This causes the `.decode('utf-8')` method to fail since it expects a byte-like object instead of a MagicMock.

### Bug Fix Strategy:
To fix this bug, we need to ensure that the output from `proc.stdout.read()` is correctly captured as a byte-like object before decoding it to a string.

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we use `proc.communicate()` to capture the stdout output as a byte-like object, which can then be decoded to a string. This should prevent the issue of receiving a MagicMock object and resolve the bug.