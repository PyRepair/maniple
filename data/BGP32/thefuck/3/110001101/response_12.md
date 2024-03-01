### Analysis
The `info` function in the `Fish` class is attempting to retrieve the version of the Fish shell by running a subprocess and capturing the output. However, the output is not being handled correctly, leading to incorrect results.

### Error
The issue lies in how the `stdout` from the subprocess is read and decoded. The function `proc.stdout.read().decode('utf-8')` is causing the issue by attempting to decode the output before reading it.

### Bug Cause
The bug occurs because the output should be read first and then decoded. By decoding before reading, the function is trying to decode an empty string resulting in an incorrect version value.

### Fix Strategy
To fix the bug, the output from the subprocess should first be read and then decoded. This will ensure that the correct version value is retrieved.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By swapping the `decode('utf-8')` after the `read()` function call, the bug should be fixed and the correct version of the Fish shell will be returned.