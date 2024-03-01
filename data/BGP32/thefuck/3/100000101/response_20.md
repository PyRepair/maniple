The bug in the provided function is that it directly reads the stdout from the `Popen` process without waiting for the process to finish, which can lead to inconsistent or incomplete output. Instead, we should wait for the process to complete before reading its output.

To fix the bug, we can use the `communicate()` method of the `Popen` object. This method waits for the process to finish and then returns a tuple of `(stdout_data, stderr_data)`.

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

This corrected version ensures that the function waits for the process to finish before capturing its output, thus providing consistent and complete results.