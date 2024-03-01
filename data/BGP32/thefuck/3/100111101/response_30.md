### Analysis:
1. The buggy function is trying to retrieve the Fish shell version by running the command `fish -c 'echo $FISH_VERSION'`.
2. The failing test sets the expected output version to `'Fish Shell 3.5.9'`.
3. The failing test fails due to a mismatch in the version format between the actual output `'Fish Shell fish, version 3.5.9'` and the expected output `'Fish Shell 3.5.9'`.

### Bug:
The bug lies in how the version string is extracted from the output of the command. The function currently appends `'Fish Shell'` to the version string returned by the command without processing the output correctly.

### Fix:
To fix the bug, we need to modify the code to extract only the version number from the output of the command and format it correctly with `'Fish Shell'`.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the version string at `', version '`, we can extract only the version number. This corrected version should now pass the failing test.