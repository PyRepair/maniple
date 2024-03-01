The bug in the `info` function arises from the mismatch between the command used to retrieve the Fish shell version and the parsing of the output. The function is currently using the command `echo $FISH_VERSION` to get the Fish shell version, but it should be using `fish --version` instead.

The corrected version of the function should also properly parse the output to extract just the version number.

Here is the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]
    return u'Fish Shell {}'.format(version)
```

With this change, the function will now execute the correct command to get the Fish shell version and parse the output to extract just the version number. This corrected version should now pass the failing test.