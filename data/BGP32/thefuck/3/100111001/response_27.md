### Bug Explanation:
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The function executes `fish -c 'echo $FISH_VERSION'` which outputs the version with additional text "fish, version" before the actual version number. This causes the comparison in the test to fail because the expected output is just the version number without the additional text.

### Fix Strategy:
To fix the bug, we need to update the command to only output the version number without any additional text like "fish, version".

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(" ")[2]
    return u'Fish Shell {}'.format(version)
```