### Analysis:
- The `info` function in the `fish.py` file is attempting to retrieve the Fish shell version using the command `echo $FISH_VERSION`, but the test is expecting the version to be retrieved using the `--version` flag.
- The test is mocking the output of the command `fish, version 3.5.9` but the `info` function is trying to read the version without the proper flag.
- The error message highlights that the expected output has extra text (`'Fish Shell fish, version 3.5.9'`) compared to the actual output (`'Fish Shell 3.5.9'`).

### Bug Cause:
- The `info` function in the `fish.py` file is not using the correct command to retrieve the version of the Fish shell, leading to a mismatch between the expected and actual outputs in the test.

### Suggested Fix:
- Update the `info` function in the `fish.py` file to use the command `fish --version` to retrieve the version of the Fish shell.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1])
```

By using the corrected version provided above, the `info` function will retrieve the Fish shell version properly by using the `--version` flag instead of trying to extract it from the `FISH_VERSION` environment variable, resolving the issue and passing the failing test.