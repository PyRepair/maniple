### Analysis
1. The buggy function `info` in the `fish.py` file is attempting to retrieve the version of the Fish Shell by executing a command and capturing its output, but it is not capturing the correct command output.
2. The failing test `test_info` in `test_fish.py` sets an incorrect expected output for the function, leading to the assertion error.
3. The expected output should be `'Fish Shell 3.5.9'`, but the current implementation includes additional text before the version number.
4. The `Popen` call in the `info` function is using a different command than expected, leading to incorrect output and the failing test.
5. To fix the bug, the `Popen` command in the `info` function should be modified to retrieve the correct version information.

### Bug Cause
The `info` function in `fish.py` is executing the command `echo $FISH_VERSION` to retrieve the version of Fish Shell. However, the test `test_info` is setting the expected output to `'Fish Shell 3.5.9'`, while the actual output includes additional text (`fish, version`). This discrepancy causes the assertion error.

### Fix Strategy
1. Amend the `info` function to execute the correct command to retrieve the Fish Shell version.
2. Update the test `test_info` to match the corrected output of the `info` function.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return 'Fish Shell {}'.format(version)
```

In the corrected version, the `Popen` command within the `info` function is modified to execute `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`. The output is also formatted correctly to match the expected values in the test.

This correction should resolve the assertion error and align the function's output with the test expectations.