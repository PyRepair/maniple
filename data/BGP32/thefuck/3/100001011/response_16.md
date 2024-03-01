The bug in the provided function is the usage of `proc.stdout.read()` before waiting for the process to finish. This can lead to hanging the process when reading from the stdout. 

To fix the bug, we need to wait for the process to finish before reading from its stdout. We can achieve this by adding `proc.wait()` before reading from `proc.stdout`.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By adding `proc.wait()` before reading from `proc.stdout`, we ensure that we only read from the stdout after the process has completed, resolving the hanging issue mentioned in the GitHub report.