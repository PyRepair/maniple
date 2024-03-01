### Analysis
The buggy function's current implementation is trying to read the output of the `Popen` process directly without waiting for the process to finish. This can lead to issues where the process output is not yet available for reading.

### Bug
The bug in the function is that it tries to read from the `proc.stdout` before the process has finished. This can cause inconsistency in fetching the output and result in an empty string.

### Fix Strategy
To fix this issue, we need to wait for the process to finish before trying to read its output. One way to do this is by using the `communicate()` method of the process.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    outs, errs = proc.communicate()
    version = outs.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```