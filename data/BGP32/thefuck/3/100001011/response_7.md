The bug in the `info` function is likely caused by the usage of `proc.stdout.read().decode('utf-8')`, which can lead to a hanging process and potential recursive loop as mentioned in the GitHub issue. To fix this issue, it is important to properly handle the process execution and reading from the stdout stream.

Here is a corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    try:
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the process to finish
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
    except Exception as e:
        return "Error retrieving Fish Shell version: {}".format(str(e))
```

In this corrected version, we are using `proc.wait()` to ensure that the process finishes before reading from the stdout stream. This should help prevent hanging processes and potential recursive loop issues. Additionally, we have added exception handling to handle any errors that might occur during the process execution or reading from the stdout stream.

By making these changes, the `info` function should now be able to retrieve the Fish Shell version without causing any hanging or recursive loop issues.