The bug in the provided function `info` lies in how the output of the `Popen` command is being handled. The function is expecting the `Popen` object to have its stdout as a byte stream, but it is not being handled correctly.

The correct approach to fixing this bug would be to wait for the process to complete and then retrieve the output using the `communicate()` method of the `Popen` object.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that the output of the `Popen` command is correctly captured after waiting for the process to complete using `communicate()` method. This approach fixes the bug and satisfies the expected input/output values.