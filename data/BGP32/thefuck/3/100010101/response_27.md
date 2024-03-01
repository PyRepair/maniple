### Strategy for fixing the bug
The bug in the `info` function arises from the incorrect extraction of the shell version from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation is not correctly decoding the output and extracting the version number.

To fix the bug, we need to ensure that the output is properly decoded and parsed to extract the version number before formatting it into the desired output string.

### The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

By splitting the output on the comma and then stripping any whitespace, we can extract just the version number from the output. This corrected version of the function should now pass the failing test case.