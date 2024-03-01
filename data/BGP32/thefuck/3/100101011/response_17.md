### Analysis:
1. The `info` function is supposed to return the name and version of the current shell. It calls `Popen` to execute a shell command to get the version of Fish shell.
2. The test case `test_info` sets up the mock behavior for `Popen` to return the version of Fish shell in the correct format.
3. The bug seems to be related to the command being executed (`echo $FISH_VERSION`) not matching the expected output format (`fish, version 3.5.9`).
4. The `Popen` arguments should be adjusted to match the command used for retrieving the version in the test case.

### Bug Cause:
The `Popen` call in the `info` function is using the wrong command (`echo $FISH_VERSION`) to retrieve the version of Fish shell. This mismatch causes the returned version to be incorrect and fails the test. The correct command to retrieve the version is `fish --version`.

### Fix Strategy:
Adjust the `Popen` call in the `info` function to execute the correct command (`fish --version`) to retrieve the version of Fish shell. This change will align the function's behavior with the expected output in the test case.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

By making this correction, the `info` function will correctly retrieve the version of the Fish shell using the `fish --version` command, leading to the expected output and passing the test case.