Based on the runtime and expected values provided, it seems that the issue lies with the version string obtained from the output of the `echo $FISH_VERSION` command not being processed correctly.

The `version` variable seems to have the prefix 'fish, version' along with the actual version number, which is causing the discrepancy in the output. The expected output should only contain the version number without any additional text.

To fix this bug, we need to remove the extra text 'fish, version' from the `version` variable before returning it in the desired format.

Here is the corrected version of the `info` function:

```python
# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number from the output
        version = version.replace('fish, version ', '')
        return u'Fish Shell {}'.format(version)
```

This correction removes the unnecessary prefix 'fish, version' from the version string obtained, ensuring that only the version number is included in the output. This modification should resolve the issue reported on GitHub related to possible recursive loops triggered by the incorrect output format.