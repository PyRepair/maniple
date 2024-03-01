## Analysis
1. The buggy function `info` is trying to retrieve the version of the current shell by running the command `echo $FISH_VERSION` in the Fish shell.
2. The failing test is trying to mock the output of `Popen` to simulate running the command and check if the version is correctly parsed.
3. The bug is caused by the fact that the command passed to `Popen` (`['fish', '-c', 'echo $FISH_VERSION']`) does not match with what the test expects (`['fish', '--version']`). This leads to incorrect output and assertion failure.
4. To fix the bug, we need to modify the command passed to `Popen` to match the expected command in the test.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return 'Fish Shell ' + version.split(", ")[1]
```

By changing the command passed to `Popen` to `['fish', '--version']`, we align the function with the test's expectation. Additionally, we adjust the return statement to extract the version number correctly from the output. This corrected version should now pass the failing test and resolve the issue reported on GitHub.