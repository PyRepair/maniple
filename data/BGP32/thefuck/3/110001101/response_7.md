### Analysis
The buggy function `info` is using `proc.stdout.read()` directly to read the output, but it is not the correct approach. The `Popen` object needs to wait for the process to complete before reading the output. This is likely causing the issue where the output is not what is expected.

### Bug Cause
The bug is caused by directly reading from `proc.stdout` before the process has completed. This results in incorrect or incomplete output being read.

### Fix Strategy
To fix the bug, we need to wait for the process to complete before reading the output. We can achieve this by using `communicate()` method of the `Popen` object, which will wait for the process to finish and then provide the output.

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