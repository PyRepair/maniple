### Analysis
The buggy function `info` is trying to retrieve the version of the Fish shell by executing a command and capturing the output. However, the current implementation of reading the output from the process using `proc.stdout.read().decode('utf-8').strip()` is not handling the output correctly, as indicated by the runtime and expected values.

### Error Location
The error lies in how the function is reading and decoding the output from the process. The expected version value is `'3.5.9'`, but the current implementation is returning `'fish, version 3.5.9'`.

### Cause of the Bug
The bug is caused by not properly handling the output of the command executed in the Fish shell.

### Fix Strategy
To fix the bug, we need to modify how the function reads and processes the output from the process so that it captures only the version number without any additional text.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

This corrected version reads the output from the process, splits it by space, and takes the last element (which should be the version number) to return the expected result.