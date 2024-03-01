### Analysis
The buggy function `info` in the `Fish` class is supposed to return the version of the fish shell. In the failing test case, the function is returning the entire version string which includes unnecessary text like `'fish, version'`. The expected output should only be the version number.

### Bug Location
The bug is located in the line:
```python
return u'Fish Shell {}'.format(version)
```
Here, the `version` string still contains the unnecessary text `'fish, version'`, which causes a mismatch in the test assertion.

### Cause of the Bug
The bug is caused by the incomplete extraction of the version number from the output of the command. The `version` variable is holding the entire output string 'fish, version 3.5.9' instead of just the version number '3.5.9'. This leads to the incorrect comparison during the test.

### Fix Strategy
To fix this bug, we need to extract just the version number from the `version` string before formatting it into the return statement. This can be done by splitting the string on space and taking the last element, which is the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will properly extract and return just the version number without the unnecessary text. This should resolve the failing test case and satisfy the expected behavior.