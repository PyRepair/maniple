### Analysis
The `info` function in the `fish.py` file is meant to retrieve the version of the Fish shell, but it is incorrectly grabbing the version string alongside other text. This issue causes the test to fail as it expects only the version number.

### Bug Explanation
The bug arises because the function `Popen.return_value.stdout.read` is being set to `[b'fish, version 3.5.9\n']`, which includes additional text ("fish, version") that is not expected in the output. This extra text leads to the mismatch between the expected output `'Fish Shell 3.5.9'` and the actual output returned by the function.

### Fix Strategy
To fix this bug, we need to modify the `info` function in `fish.py` to extract only the version number from the output obtained from the shell command.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

In this corrected version, `split()[2]` is used to extract the third element from the split version string, which isolates the version number. This change ensures that only the version number is included in the final output.