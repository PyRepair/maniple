The bug in the provided function is that it is not handling the subprocess properly to get the shell version. The `Popen` object needs to wait for the command to finish executing before reading the output.

The strategy for fixing the bug is to add `proc.wait()` after executing the command to make sure the process has finished and then read the output.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```