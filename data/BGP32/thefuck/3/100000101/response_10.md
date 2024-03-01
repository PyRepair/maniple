The bug in the provided function is that it is trying to read from the `proc.stdout` before waiting for the process to finish executing. This can lead to an incomplete or empty output being read.

To fix this bug, we should use the `communicate()` method of the subprocess.Popen object which will wait for the process to finish and then read the output.

Here is the corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that the function waits for the process to finish before reading the output, thus providing the correct version information.