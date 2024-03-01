### Explanation of the Bug

The bug in the `info` function arises due to the incorrect command being used to retrieve the version information of the Fish shell. The command being executed is `'fish -c 'echo $FISH_VERSION'`, which returns a string in the form `'fish, version X.X.X'`. This string is then processed to extract the version number, resulting in `'X.X.X'`.

However, the comparison in the test is against the expected value `'Fish Shell 3.5.9'`, which does not match the extracted version number format. This discrepancy causes the assertion to fail.

### Fix Strategy

To fix this bug, we need to modify the command used to obtain the Fish shell version so that it returns the version number directly without any additional text. Then, the extracted version number can be used to format the correct output string for comparison in the test.

### Corrected Version of the Function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')
    return f'Fish Shell {version}'
```

In the corrected version, the command 'fish --version' is used to obtain the version information directly. The extracted version number is then formatted into the expected output string 'Fish Shell X.X.X'. This correction ensures that the function returns the correct version format for comparison in the test, resolving the failing assertion.