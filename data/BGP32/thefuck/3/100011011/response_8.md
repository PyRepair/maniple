### Analysis:
The provided buggy function `info` is attempting to get the version of the Fish shell by running `echo $FISH_VERSION` command. The issue arises from the fact that the output of the `echo $FISH_VERSION` command includes the word "fish, version" before the actual version number. This causes the assertion error in the failing test as the expected output doesn't include the word "fish, version."

### Bug Cause:
The bug is caused by the incorrect parsing of the output from the `echo $FISH_VERSION` command. The `info` function should only return the version number without the additional "fish, version" text.

### Fix Strategy:
To fix the bug, we need to modify the parsing logic to extract only the version number from the command output and format it correctly.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output of the `echo $FISH_VERSION` command and extracting the last part as the version number, we can correctly format the output as "Fish Shell {version}". This corrected version should now pass the failing test and resolve the issue reported on GitHub.