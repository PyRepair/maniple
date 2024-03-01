### Explanation:
The bug in the provided function lies in how the `proc.stdout.read()` method is used. In the buggy function, the `proc.stdout.read()` method is called before the process finishes running, which can lead to incorrect or incomplete output being read.

### Bug Fix Strategy:
To fix this bug, we need to wait for the process to finish running and then read the output. This can be achieved by using the `communicate()` method of the `Popen` object to wait for the process to finish and retrieve the output.

### Corrected Version:
Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()` instead of `proc.stdout.read()`, we ensure that the process finishes running before reading the output, thus fixing the bug.