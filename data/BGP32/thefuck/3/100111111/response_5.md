### Analysis
1. The buggy function `info` in `fish.py` tries to get the version of Fish shell by running a command. However, the command used is `echo $FISH_VERSION`, which does not match the expected output format in the test.
2. The failing test sets the side effect of `Popen.return_value.stdout.read` to `b'fish, version 3.5.9\n'`, but the function `info` expects only the version number without the additional text.
3. The failing test compares the actual output `Fish Shell fish, version 3.5.9` with the expected output `Fish Shell 3.5.9`, resulting in an assertion error due to the mismatch.
4. To fix the bug, the command used to retrieve the Fish shell version should be modified to align with the expected output format.

### Bug Fix Strategy
- Update the command executed by `Popen` to retrieve only the version number without additional text.
- Modify the format string used to return the version in the `info` function.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(' ')[-1]  # Extract only the version number
    return f'Fish Shell {version}'
``` 

Now, the `info` function retrieves the version number only and returns it in the correct format. This correction should align with the expected output of the failing test and resolve the GitHub issue related to the bug.