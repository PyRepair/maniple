### Bug Explanation
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `'echo $FISH_VERSION'` does not actually return the Fish shell version string directly, leading to the incorrect extraction of the version. Additionally, the test is expecting the version string to start with the string 'fish, version', which is not present in the actual output.

### Bug Fix Strategy
1. Update the command in the `Popen` call to retrieve the Fish shell version properly.
2. Modify the test to match the correct version format.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

After applying the corrected version of the `info` function, the test should now pass without any issues.