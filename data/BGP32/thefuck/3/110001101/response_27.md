### Explanation:
The bug in the `info` function lies in the way it reads and processes the output from the `Popen` process. The `proc.stdout.read()` call returns a byte string containing the output of the process, which needs to be decoded before stripping and using it. However, the current implementation is directly calling `proc.stdout.read()` without decoding it first, leading to incorrect processing and output.

### Strategy for Fixing the Bug:
To fix the bug, we need to correctly decode the byte string output obtained from `proc.stdout.read()` using the appropriate encoding before stripping and using it. This ensures that we get the expected version string without any issues with encoding.

### Corrected Version of the Function:
```python
# The corrected version of the function
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will properly decode the output before extracting and using the version information, leading to the correct output.