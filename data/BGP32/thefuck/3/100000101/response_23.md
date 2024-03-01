The bug in the provided function is caused because the `Popen` object is not properly handled before reading from its output. The `proc.stdout.read()` call is directly applied without waiting for the process to finish, leading to potential issues in retrieving the correct output.

To fix this bug, it is necessary to wait for the process to complete before reading from its output. This can be achieved by adding `proc.communicate()` before attempting to read from the output.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.communicate()  # Wait for the process to finish
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this fix, the function now properly waits for the process to complete before reading the output, ensuring that the correct shell version is retrieved.