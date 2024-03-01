### Explanation:
The bug in the provided function lies in the way it reads the output from the Popen process. The `proc.stdout.read()` method returns a `bytes` object, and then the function tries to decode it using `decode('utf-8')` to convert it into a string. However, in the buggy function, the decoding and stripping operations are not handled correctly, which causes issues with processing the output.

### Strategy for fixing the bug:
To fix the bug, we need to properly handle the decoding and stripping of the output obtained from `proc.stdout.read()`. This involves decoding the bytes to a string using the correct encoding format and then stripping any leading or trailing whitespace characters.

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

In the corrected version, `proc.communicate()` is used to retrieve the output and error streams of the process. Then, the output is properly decoded to a string using `decode('utf-8')` and stripped of any leading or trailing whitespace with `strip()`. This ensures that the function correctly processes the shell version output and returns the expected result.