The bug in the provided function is that the `Popen` object is not being communicated with properly to obtain the output version of Fish shell. The function is trying to read the output directly from `proc.stdout`, but this is not the correct way to retrieve the output.

To fix this bug, we need to use the `communicate()` method of the `Popen` object, which will allow us to properly read the output. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now properly retrieve and return the version of Fish shell as expected.