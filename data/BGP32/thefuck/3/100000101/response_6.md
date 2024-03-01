The bug in the provided function lies in the handling of the Popen object and its stdout. The function is trying to read from proc.stdout directly without waiting for the process to finish or handling any potential errors.

To fix this bug, we should wait for the process to finish and handle any exceptions that may occur during the process execution. We can achieve this by calling the `proc.communicate()` method, which waits for the process to finish and returns a tuple of stdout and stderr. 

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip() if stdout else ""
    return u'Fish Shell {}'.format(version)
```

By waiting for the process to finish and handling the stdout properly, the corrected function should now return the version of the Fish Shell correctly.