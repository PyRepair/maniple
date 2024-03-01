The bug in the provided function is that the `proc.stdout.read()` method is being called before the subprocess has finished executing, which results in an empty string being returned instead of the actual version of the Fish shell.

To fix this bug, we need to wait for the subprocess to finish executing before reading its output. We can achieve this by adding `proc.wait()` after starting the subprocess with `Popen`.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the subprocess to finish executing
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that we only read the output of the subprocess after it has completed execution, thereby returning the correct version of the Fish shell.