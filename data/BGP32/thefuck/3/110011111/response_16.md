The bug in the provided function `info` lies in how the version string fetched from the subprocess is processed. The current implementation includes the text `"fish, version"` in the version string extracted from the command output, causing the incorrect comparison in the test.

To address this bug, we need to modify the function to extract only the version number from the output.

Here is the corrected version of the `info` function:

```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')  # Remove unnecessary text
        return u'Fish Shell {}'.format(version)
```

By adding the `replace('fish, version ', '')` method call to remove the extra text from the version string, the function now extracts and returns only the version number. This modification ensures that the comparison in the test will be correct, and the function will return the expected output.

This version of the `info` function should now pass the failing test and align with the expected input/output values.