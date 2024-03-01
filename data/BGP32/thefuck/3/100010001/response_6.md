### Analysis:
- The error message indicates that the expected output from the `shell.info()` function is `'Fish Shell 3.5.9'`, but the actual result produced is `'Fish Shell fish, version 3.5.9'`.
- The `Popen` mocking behavior is correctly set up in the test, but the issue seems to be with the parsing and formatting of the output.
- The function is supposed to extract the version number from the output of the `$FISH_VERSION` environment variable.

### Bug Cause:
- The bug is caused by the incorrect formatting of the version string fetched from the output of the command.
- The string `'fish, version 3.5.9\n'` is not correctly stripped or parsed to extract only the version number.

### Fix Strategy:
- To fix the bug, we need to correctly parse and extract only the version number from the output string.
- We should make sure to remove the unnecessary characters like 'fish, version' and '\n'.

### Correction:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    # Extract the version number from the output
    version = output.split()[2]
    return u'Fish Shell {}'.format(version)
```

### Correction Rationale:
1. The `split()` method is used to split the output string into separate words.
2. The version number is extracted from the list of words by indexing the third element (assuming the format `'fish, version x.x.x'`).
3. This corrected code snippet ensures only the version number is used to format the final string.
4. This updated version should produce the expected output `'Fish Shell 3.5.9'` and pass the failing test scenario.