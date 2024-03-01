### Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION` and then formatting it with the shell name. However, the issue lies in the handling of the `proc` object and reading its output. The function is trying to read from `proc.stdout`, but the read function needs to be called to actually obtain the output.

### Bug
The bug in the current implementation is that `proc.stdout.read()` is not being actually called to read the output from the process.

### Fix
We need to modify the line `version = proc.stdout.read().decode('utf-8').strip()` to actually call the `read()` function before decoding the output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return f'Fish Shell {version}'
```