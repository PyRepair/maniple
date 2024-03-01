### Analysis
The buggy function `info` is attempting to retrieve the Fish Shell version by executing a command using `Popen` and reading the output. However, the command used to retrieve the version (`'echo $FISH_VERSION'`) does not match what is being asserted in the test function (`['fish', '--version']`). This mismatch causes the test to fail with an incorrect assertion error.

### Bug Cause
The bug is caused by the incorrect command (`'echo $FISH_VERSION'`) used to retrieve the Fish Shell version in the `info` function, which does not match the expected version output (`'fish, version 3.5.9\n'`) in the test.

### Fix Strategy
To fix the bug, update the command in the `Popen` call within the `info` function to match the expected output. Using the command `['fish', '--version']` will ensure that the correct version information is retrieved.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

By updating the `Popen` command in the `info` function to `['fish', '--version']`, the function will correctly retrieve and format the Fish Shell version information. This change ensures that the test will pass with the expected output.