### Analysis
1. The `info` function within the `fish.py` file aims to extract the version number of the Fish Shell by running the command `fish -c 'echo $FISH_VERSION'`.
2. The test function `test_info` in `test_fish.py` simulates the output of the command and expects the function to return the correct version number.
3. The issue on GitHub suggests that the current implementation causes a recursive loop within the Oh-My-Fish plugin due to incorrect shell initialization.

### Bug Cause
The bug likely stems from the mismatch between the command used to retrieve the version number (`echo $FISH_VERSION`) and the expected version number in the test. The test expects `3.5.9`, but the command outputs `fish, version 3.5.9`, leading to a failing test.

### Fix Strategy
To fix the bug, we should modify the command or manipulate the obtained version to match the expected output in the test function.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[2]
    return u'Fish Shell {}'.format(version)
```

With this corrected version of the `info` function, the command used to retrieve the version number is changed to `fish --version`, and then the version number is extracted from the obtained output. The returned version will now match the expected output in the test, resolving the bug.