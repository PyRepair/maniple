### 3. Explanation of the Bug

The bug in the `info` function of the `Fish` class is caused by the mismatch between the expected version format `'3.5.9'` and the actual version format `'fish, version 3.5.9'`. The `info` function is supposed to extract the version number of Fish shell, but it fails to format the extracted version correctly.

The failing test expects `'Fish Shell 3.5.9'` as the output of the `info` function, but the actual value is `'Fish Shell fish, version 3.5.9'`. This discrepancy in version formatting leads to the assertion error in the test.

### 4. Fixing the Bug

To fix the bug, the `info` function should properly parse the version string to extract only the version number (`'3.5.9'`) and format it correctly as `'Fish Shell 3.5.9'`.

### The corrected function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split()[-1]
    return 'Fish Shell {}'.format(version)
```

In this corrected version, the `info` function now calls `Popen(['fish', '--version'])` to get the version string directly, splits the string by whitespace and takes the last element as the version number. It then formats the version number properly and returns it as `'Fish Shell 3.5.9'`.

This corrected version should pass the failing test and align with the expected input/output values.

By applying this fix, the `info` function will now correctly extract and format the Fish shell version, ensuring the test passes successfully.