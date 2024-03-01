### Analysis
The buggy function `info` tries to get the current shell's version by running `fish -c 'echo $FISH_VERSION'` and then extracting the version information. However, the test case `test_info` sets the return value of `proc.stdout.read` to `b'fish, version 3.5.9\n'`, which includes extra information before the version number that causes the mismatch.

### Bug Cause
The bug is caused by the discrepancy between the expected version format `'3.5.9'` and the actual format `'fish, version 3.5.9'`. This difference leads to the test failing as it expects the version number only without any additional text.

### Fix Strategy
To fix the bug, we need to modify the `info` function to extract and return only the version number without any extra information. We can achieve this by splitting the string on spaces and taking the last element as the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

This corrected version ensures that only the version number `3.5.9` is extracted from the output, which aligns with the expectations of the test case.