### Bug Explanation
The bug in the `info` function is caused by the fact that the command used to retrieve the Fish shell version is incorrect. The command `'echo $FISH_VERSION'` does not provide the version number in the expected format, resulting in the incorrect version value `'fish, version 3.5.9'`.

### Bug Fix Strategy
To fix the bug, we need to change the command used to retrieve the Fish shell version to `'fish --version'` which provides the version number in the correct format.

### Corrected Version of the Function
```python
# The corrected version of the function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the function should now correctly extract and format the Fish shell version for the expected output.