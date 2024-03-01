### Bug Analysis:
The buggy function `info` in the `fish.py` file is supposed to return the version of the Fish Shell. The issue arises because the function is extracting the version string directly from the command output without proper parsing, leading to the incorrect result.

- The function is currently returning the entire output `'fish, version 3.5.9'` instead of just the version number `'3.5.9'`.
- The assert statement in the failing test is comparing the full output with the expected version number, causing the test to fail.

### Bug Fix Strategy:
To fix the bug, we need to modify the function to extract and return only the version number from the command output. We will strip the unnecessary parts of the output and only keep the version number.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```

### Explanation:
- `.split(", version ")` is used to split the output line based on `", version "` and extract the version number.
- `[1]` is used to access the second part of the split result, which contains the version number only.
- Now the function will return only the version number without any additional text, satisfying the expected output format.

By making this modification, the corrected function should now return the version number only, allowing the test to pass successfully.