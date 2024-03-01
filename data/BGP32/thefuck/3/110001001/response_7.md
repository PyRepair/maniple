### Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell by executing a command. However, it seems to be encountering issues with reading the output from the process.

### Bug
The bug in the `info` function is caused by calling `proc.stdout.read()` without waiting for the process to complete, leading to an empty or incomplete output.

### Fix
To fix the bug, we need to wait for the process to finish before reading its output. We can achieve this by calling `proc.communicate()` which will wait for the process to finish and then read the output.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        output, _ = proc.communicate()
        version = output.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```