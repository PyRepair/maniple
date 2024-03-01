### Explanation of the Bug
The bug in the provided function lies in how the output of the `proc.stdout.read()` method is being handled. The `proc.stdout.read()` method returns a `bytes` object, which needs to be decoded into a string before calling the `strip()` method on it. However, the code is trying to call `strip()` directly on the `bytes` object, leading to a decoding error.

### Fixing the Bug
To fix the bug, we need to ensure that the output of `proc.stdout.read()` is decoded into a string before further processing. This can be achieved by using the `decode('utf-8')` method on the `bytes` object. 

### Corrected Version of the Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    version = version_bytes.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

With this correction, the function should now properly decode the output from the command execution and return the expected result.