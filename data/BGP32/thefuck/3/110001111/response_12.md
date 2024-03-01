Based on the provided information, the bug in the `info` function of the `Fish` class is caused by the fact that the output of the `echo $FISH_VERSION` command includes the string `fish, version` along with the version number. This discrepancy leads to incorrect parsing and formatting of the version number.

To fix this bug, we need to modify the parsing logic to extract only the version number from the command output. We can achieve this by splitting the output based on the comma and space characters, and then taking the second part which contains the version number.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", ")[1]
        return u'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract the version number from the output of `echo $FISH_VERSION` command and return the expected result. This fix addresses the issue mentioned in the GitHub report related to the recursive loop triggered by the incorrect parsing of the Fish shell version.