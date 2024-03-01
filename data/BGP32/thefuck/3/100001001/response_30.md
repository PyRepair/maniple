### Explanation of the bug

The bug in the `info` function occurs because the `proc.stdout.read()` function returns a `MagicMock` object instead of the actual output string. This `MagicMock` object cannot be decoded using `'utf-8'` and results in an incorrect version string.

### Fixing the bug

To fix the bug, we need to read the output from the `proc.stdout` correctly and decode it as a UTF-8 string before stripping it. We can also handle potential errors during the decoding process.

### Corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    try:
        version = output.decode('utf-8').strip()
    except UnicodeDecodeError:
        version = "unknown"
    return u'Fish Shell {}'.format(version)
``` 

In this corrected version, we utilize the `proc.communicate()` method to read the output from the subprocess. We then decode the output using UTF-8 encoding and strip any whitespace characters to obtain the correct version string. Additionally, if there are any Unicode decoding errors, we handle them by setting the version to "unknown".