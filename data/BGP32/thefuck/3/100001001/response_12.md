### Bug Explanation
The bug in the provided function lies in how it handles reading the output from the subprocess. The `proc.stdout.read()` method returns a `bytes` object, and when decoding it to UTF-8 using `.decode('utf-8')`, it produces a string. However, in the given test case, the expectation is that the `version` variable should contain `'fish, version 3.5.9'`, which indicates that the output is not being read and decoded correctly.

### Bug Fix
To fix this bug, we need to ensure that the output from the subprocess is correctly read and decoded before returning the version. We should handle the possible encoding issues and errors that may occur during this process.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version:
- We use `proc.communicate()` to read the output and errors from the subprocess.
- We decode the output using `decode('utf-8')` to get the version as a string.
- We strip any extra whitespaces from the version string.
- We return the formatted version string including the shell name.