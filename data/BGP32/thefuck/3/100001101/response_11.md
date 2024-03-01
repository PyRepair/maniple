### Analysis
The buggy function `info` is trying to extract the version of the Fish shell by running a command `fish -c 'echo $FISH_VERSION'` using the `Popen` function. However, the current implementation is not correctly capturing the version due to incorrect handling of the output from the `Popen` process.

### Bug
The bug lies in how the function is trying to read the output from the `Popen` process. It calls `proc.stdout.read()` directly without waiting for the process to finish or handling any potential errors.

### Fix
To fix the bug, we need to wait for the process to finish by calling `proc.communicate()` and then read the output from the process. Additionally, we need to handle any errors that may occur during the process execution.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By using `proc.communicate()` to wait for the process to finish and capturing the output correctly, we ensure that the function returns the expected version of the Fish shell.