### Analysis:
The buggy function `info` is intended to return the name and version of the current Fish Shell by executing the command `fish -c 'echo $FISH_VERSION'`. However, the test is failing because the function is not correctly handling the output of the command, leading to an incorrect version format.

### Error Location:
The error likely lies in the way the `version` variable is being extracted from the output of the `fish -c 'echo $FISH_VERSION'` command.

### Bug Explanation:
The buggy function is reading the output of the command `echo $FISH_VERSION` and not parsing the output correctly to extract just the version number. As a result, the `version` variable contains `'fish, version 3.5.9'` instead of just `'3.5.9'`.

### Bug Fix Strategy:
To fix the bug, we need to correctly parse the output of the `echo $FISH_VERSION` command to extract only the version number from the output string.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract only the version number from the output of the command, resolving the issue with the failing test.