### Explanation:
The bug in the `info` function arises from how the output of the `Popen` process is being handled. The `proc.stdout.read()` method is being called, but it returns a MagicMock object instead of the actual output of the command.

### Strategy for fixing the bug:
To fix this bug, we need to modify the way we read the output of the `Popen` process to correctly capture and decode the actual output of the command.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output, _ = proc.communicate()
    version = output.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version:
- We use the `communicate()` method of the `Popen` process to obtain the output and error streams of the process.
- We decode the output stream to get the actual version of the shell.
- We return the correct formatted version information.