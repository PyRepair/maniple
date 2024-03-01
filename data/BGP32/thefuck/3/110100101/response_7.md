### Strategy for fixing the bug:
The bug in the `info` function is caused by reading the standard output of the `Popen` process without waiting for it to finish. This can lead to empty or incomplete output being read. To fix this, we need to wait for the process to finish before reading the standard output.

### Corrected version of the `info` function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By adding the `proc.wait()` line before reading the output, we ensure that the process has finished executing and the output is complete before reading it. This will fix the bug and the function will return the correct output.