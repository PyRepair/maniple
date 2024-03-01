### Analysis
- The `info` function is intended to return the name and version of the current shell, retrieved using a `Popen` subprocess to execute a command in the Fish Shell.
- The function currently expects the command to return the output of `FISH_VERSION`, but the test is verifying against `'fish, version 3.5.9\n'`, which contradicts the command used in the function.
- The function is attempting to read the output from the subprocess but might not be reading it correctly.

### Bug Explanation
- The bug in the function arises from the discrepancy between the command used in the function (`echo $FISH_VERSION`) and the expected output in the test (`'fish, version 3.5.9\n'`). This inconsistency leads to incorrect output when reading the subprocess results.

### Fix Strategy
1. Modify the command in the `Popen` subprocess call to match the expected output in the test case (`'fish --version'`).
2. Update the logic in the function to correctly read the output of the subprocess.
3. Strip any unnecessary characters from the version string to match the expected output.

### Corrected Version
```python
# The corrected version of the function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return 'Fish Shell {}'.format(version)
```

In this corrected version, the command in the `Popen` call is changed to `['fish', '--version']` to align with the expected test output. Additionally, the logic to extract the version number is updated to correctly handle the output format.