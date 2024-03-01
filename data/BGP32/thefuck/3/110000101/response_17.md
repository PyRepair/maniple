### Analysis
The buggy function `info` is attempting to retrieve the version of the Fish shell using a subprocess. However, the issue lies in how the function is handling the subprocess output. The `proc.stdout.read().decode('utf-8').strip()` is not correctly processing the output.

### Bug Cause
The bug is caused by not waiting for the subprocess to finish properly before reading its output. This leads to an empty string being returned as the version, resulting in incorrect output.

### Fix Strategy
To fix the bug, we need to ensure that the subprocess output is properly captured and decoded after the subprocess has completed running.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

In the corrected version, `proc.communicate()` is used to wait for the subprocess to finish and retrieve its output. This ensures that the version is properly captured and decoded before being returned.