### Analysis
The buggy function `info` is attempting to get the version of the Fish shell by executing a command using `Popen`. However, it is not handling the process execution correctly, resulting in incorrect output.

### Bug
The bug in the function is that it is not waiting for the process to complete before trying to read the output. As a result, the `proc.stdout.read()` is being called before the process completes, leading to incorrect or no output.

### Fix
To fix the bug, we need to ensure that the process has completed before reading the output. This can be achieved by adding `proc.communicate()` after creating the process, which will wait for the process to finish before proceeding.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.communicate()  # Wait for the process to complete
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```