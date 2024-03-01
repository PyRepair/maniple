## Analysis
1. The buggy function `info` in the `fish.py` file is supposed to return the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'` and extracting the version from the output.
2. The failing test in `test_fish.py` sets up a mock for `Popen` to mimic the command output, expecting `shell.info()` to return `'Fish Shell 3.5.9'`.
3. The error occurs because the function incorrectly extracts the version string from the output, leading to a mismatch.
4. The bug is causing the function to return `'Fish Shell fish, version 3.5.9'` instead of `'Fish Shell 3.5.9'`. The issue on GitHub indicates that there is a problem with shell initialization triggering a loop.
   
## Bug Fix Strategy
To fix the bug:
- Amend the way the version string is extracted from the command output to include only the version number.
- Update the test to reflect the corrected behavior.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return f'Fish Shell {version}'
```

In the corrected version, `split(', version ')` is used to extract only the version number from the output.

By making this change, the function should now correctly return `'Fish Shell 3.5.9'` as expected.