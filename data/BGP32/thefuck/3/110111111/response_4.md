To fix the bug in the provided function, we need to correct the command used to retrieve the Fish shell version and properly format it. Based on the failing test and the expected input/output values, the issue lies in the command `['fish', '-c', 'echo $FISH_VERSION']` being used to fetch the version.

The correct command should be `['fish', '--version']` to retrieve the Fish shell version correctly. Additionally, we need to extract the version number from the output, which is currently 'fish, version x.x.x', and format it as 'x.x.x'.

Here is the corrected version of the buggy function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

With this correction, the function should now correctly extract the Fish shell version and format it as expected. It should pass the failing test and satisfy the expected input/output values.