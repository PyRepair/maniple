Based on the provided information from the runtime and expected values, as well as the GitHub issue description, the bug in the `info` function of the `fish.py` file is due to the version string extracted from the command containing unwanted text.

To fix the bug, we need to modify the command executed to only retrieve the version number without any additional text.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
    return u'Fish Shell {}'.format(version)
```

In this corrected version, the `replace('fish, version ', '')` function call removes the unwanted text "fish, version " from the extracted version string. This modification ensures that only the version number is returned, as expected.