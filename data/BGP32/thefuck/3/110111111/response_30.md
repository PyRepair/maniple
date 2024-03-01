To fix the bug in the `info` function of the `Fish` class, we need to adjust the command used to retrieve the version of the Fish shell. Currently, the command `echo $FISH_VERSION` is used, which is not the correct command to get the version string in the format required for the comparison in the test.

We need to update the command to `fish --version` to retrieve the correct version string. Additionally, since the version string fetched with this command includes extra text like "fish, version", we need to parse out only the version number for comparison.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_number = version.split(',')[1].strip().split()[-1] # Extracting only the version number
        return u'Fish Shell {}'.format(version_number)
```

This corrected version of the `info` function should now correctly extract the version number and format it as 'Fish Shell x.x.x' for comparison. This change should resolve the failing test and address the issue reported on GitHub regarding the plugin behavior in Oh-My-Fish.