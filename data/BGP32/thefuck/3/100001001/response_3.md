### Analysis
The function `info` is trying to retrieve the version of the Fish shell by running a command in the shell and capturing the output. However, the issue seems to arise from how the output is being read and decoded.

### Bug
The bug lies in how the function is attempting to read and decode the output from the `Popen` process. It is currently using `proc.stdout.read().decode('utf-8')` directly on the `stdout` attribute without considering if the process has finished executing or waiting for the output. This can lead to reading empty or incomplete output.

### Fix
To fix the bug, it is recommended to use the `communicate()` method of the `Popen` object, which waits for the command to complete and collects its output. By using `communicate()`, we can ensure that the output is correctly obtained before attempting to decode it.

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