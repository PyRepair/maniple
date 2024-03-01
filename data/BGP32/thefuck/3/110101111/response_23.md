To fix the bug in the `info` function of the `Fish` class, we need to address the following issues:
1. The command used in Popen is incorrect, it should be ['fish', '--version'] instead of ['fish', '-c', 'echo $FISH_VERSION'].
2. The format of the version string obtained from the command output needs to be modified to extract just the version number.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.split(',')[1].split()[1]
        return u'Fish Shell {}'.format(version)
```

By using `['fish', '--version']` as the command to retrieve the version, we ensure that the correct information is obtained. Additionally, the version string is properly parsed to extract only the version number.

This corrected version of the `info` function should now pass the failing test and satisfy the expected input/output values.