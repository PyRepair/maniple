### Analysis:
1. The `info()` function in `fish.py` is supposed to return the version of the Fish shell by executing a command and reading its output.
2. The function reads the output from the process and formats it as `'Fish Shell version'`, but it currently reads the value incorrectly.
3. The failing test provided in `test_fish.py` sets the expected output to 'Fish Shell 3.5.9' but it receives 'Fish Shell fish, version 3.5.9'.
4. To fix the bug, the function should read the correct version and format it properly before returning.

### Bug Fix Strategy:
1. Update the command used to get the Fish shell version inside the `info()` function.
2. Properly format the version number obtained from the command.
3. Update the test case to ensure the correct output comparison.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_bytes = proc.stdout.read()
    version_str = version_bytes.decode('utf-8').strip().split(' ')[2]  # Extracting the version from the output
    return u'Fish Shell {}'.format(version_str)
```

By applying this fix, the function will correctly extract the version number from the command output and format it properly before returning. It will align with the test case's expected value 'Fish Shell 3.5.9'. This will address the bug and ensure the test case passes.