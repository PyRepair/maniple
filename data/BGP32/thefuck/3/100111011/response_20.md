## Bug Analysis
1. The `info` function in the `fish.py` file is using `echo $FISH_VERSION` to retrieve the version of the Fish shell. 
2. The test is setting the `Popen.return_value.stdout.read.side_effect` to `[b'fish, version 3.5.9\n']`.
3. The expected output for version is `'Fish Shell 3.5.9'`.
4. The error message indicates a mismatch in the output format due to the extra `'fish, version '`.
5. The GitHub issue mentions a recursive loop caused by `thefuck -v`, pointing to a potential issue with the version retrieval method.

## Bug Cause
The version extraction from the command `echo $FISH_VERSION` includes the string `'fish, version '`, causing a mismatch with the expected output format `'Fish Shell 3.5.9'`.

## Bug Fix
To fix the bug, we need to update the version extraction method to eliminate the unwanted prefix. We can modify the function to extract only the version number without the additional information.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(", version ")[1]  # Extract version number only
    return f'Fish Shell {version}'
``` 

The modified line `version = version.split(", version ")[1]` splits the string to extract only the version number without the unwanted prefix. This corrected version should pass the failing test and resolve the GitHub issue.