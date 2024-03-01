The bug in the provided function is that it is attempting to read the output of the `Popen` process directly without waiting for the process to finish. This leads to an empty output being read.

To fix this bug, we need to wait for the `Popen` process to complete before reading its output. We can achieve this by using the `communicate()` method of the process object.

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

By using the `communicate()` method, we ensure that the function waits for the `Popen` process to finish and then reads its output correctly.

This corrected version should now return the expected output values and types for the given test case.