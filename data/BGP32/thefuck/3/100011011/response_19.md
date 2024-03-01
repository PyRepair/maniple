### Bug Analysis:
The bug arises from the fact that the `info` function in the Fish shell class is not correctly parsing the output of the `echo $FISH_VERSION` command. The current implementation is returning the entire output of the command as a string which includes unnecessary text like "fish, version" that needs to be removed.

### Error Cause:
The error occurs because the expected output from the `info` function is `'Fish Shell 3.5.9'`, but the actual output includes additional text making it `'Fish Shell fish, version 3.5.9'`. This extra text is due to improper handling of the command output.

### Bug Fix Strategy:
To resolve the bug, we need to modify the `info` function to properly extract the version number from the output of the `echo $FISH_VERSION` command and construct the desired formatted string. This can be achieved by parsing the output correctly and removing any unnecessary text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the `info` function will properly extract and return the version number without any extra text, resolving the failing test case.