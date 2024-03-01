### Analysis
The bug in the `info` function lies in the way the output from the `Popen` process is being read. The code correctly executes the command to retrieve the Fish shell version, but the way it reads the output is problematic. The `stdout` attribute of the `Popen` object is being accessed multiple times, potentially causing issues in receiving the correct output.

### Bug Cause
The bug occurs because the `Popen` object's `stdout` is read multiple times. This can lead to unexpected behavior as the output might not be fully captured or processed correctly.

### Fix
To fix this bug, we can avoid reading the `stdout` multiple times by capturing its content once and then decoding it to extract the version information. Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()` to capture the output only once and then decoding it to extract the version, we ensure that the complete output is processed correctly. This approach avoids potential issues caused by reading `stdout` multiple times.