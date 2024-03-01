The bug in the provided function is that it attempts to read from `proc.stdout` before waiting for the process to finish using `proc.communicate()` or `proc.wait()`. This can lead to incomplete or empty output being read.

To fix this bug, we need to modify the function to wait for the process to finish before reading from `proc.stdout`. Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By calling `proc.wait()`, we ensure that the process completes before we attempt to read from `proc.stdout`. This should fix the bug and allow the function to return the correct version of the Fish shell.