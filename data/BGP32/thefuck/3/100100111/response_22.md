### Analysis
1. The buggy function `info` in `fish.py` is intended to return the name and version of the current Fish shell.
2. The `test_info` test function in `test_fish.py` sets up a mock for `Popen.return_value.stdout.read` to return the version string, 'fish, version 3.5.9', but the function is trying to read version using 'echo $FISH_VERSION'.
3. The current implementation of `info` uses `Popen` to execute `fish -c 'echo $FISH_VERSION'`, which is incorrect.
4. The expected behavior is to directly call `fish --version` to get the version string.

### Issue Explanation
1. The bug is caused by the incorrect command used to retrieve the Fish shell version. The function is trying to extract the version using `echo $FISH_VERSION`, which is not the correct command. It should use `fish --version` instead.
2. The failing test sets up the mock to return 'fish, version 3.5.9', but the buggy function is unable to extract the version correctly, leading to test failure.
3. The expected input is the version string 'fish, version 3.5.9', and the expected output from the function should be 'Fish Shell 3.5.9'.
4. To fix the bug, we need to modify the command used to retrieve the Fish shell version within the `info` function.

### Fix Strategy
1. Modify the command executed by `Popen` in the `info` function to directly get the Fish shell version using `fish --version`.
2. Update the `test_info` test to expect the correct version string and modify the mock accordingly.

### Corrected Function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this corrected function, the test case `test_info` should pass successfully. It retrieves the Fish shell version using `fish --version` and extracts the version number correctly.