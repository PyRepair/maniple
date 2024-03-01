The bug in the provided function arises from not waiting for the `Popen` process to finish before trying to read from its stdout. The `Popen` function returns a process object that needs to be communicated with using `communicate()` method to ensure completion.

Here's the corrected version of the function that includes this fix:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version of the function ensures that it properly waits for the process to complete before attempting to read from its stdout, addressing the bug.