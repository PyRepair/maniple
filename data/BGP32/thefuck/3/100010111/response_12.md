## Bug Analysis
1. The buggy function `info` in `fish.py` is attempting to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`.
2. The issue arises when trying to extract the version from the output, resulting in unexpected string `fish, version 3.5.9` instead of the expected `3.5.9` due to a comma in the output.
3. This discrepancy causes the assertion error during the test execution, leading to a failed test case.
4. The error is related to a GitHub issue where using `thefuck -v` with Oh-My-Fish plugin triggers a recursive loop due to this version extraction bug.

## Bug Fix Strategy
To fix this bug, we need to modify the parsing logic for extracting the version string to handle the format `fish, version 3.5.9` correctly. The fix should involve a more robust method to accurately extract and format the version number.

## Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(", version ")[-1]  # Extract version part after the comma
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now correctly extract the version number `3.5.9` from the output and return it in the expected format `'Fish Shell 3.5.9'`. This correction addresses the specific issue identified in the failing test.