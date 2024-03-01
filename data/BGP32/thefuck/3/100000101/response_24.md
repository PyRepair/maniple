The bug in the provided function is that it is not waiting for the process to complete before trying to read the output from it. This results in an empty version string being returned. The correct approach would be to use the `communicate()` method of the `Popen` object to wait for the process to finish before reading the output.

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

This corrected version ensures that the function waits for the process to complete before reading the output. It should now return the correct version string as expected.