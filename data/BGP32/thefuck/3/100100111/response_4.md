## Analysis
1. The `info` function is trying to retrieve the Fish Shell version by executing the command `fish -c 'echo $FISH_VERSION'` using `Popen`. However, the command used in the test is different, `['fish', '--version']`, causing the test to fail.
2. The bug is caused by the mismatch between the command used in the function and the test. This leads to incorrect output comparison and assertion failure.
3. The failing test expects the output `'Fish Shell 3.5.9'`, but the function is not extracting the version correctly due to the command mismatch.
4. To fix the bug, the function should use the correct command to extract the Fish Shell version matching the test case.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.readline().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

In the corrected version of the function, `'fish --version'` is used to extract the version correctly. The version is then extracted by splitting the output of `proc.stdout.readline()` and taking the last element to get the version number. This will align the function with the test case and fix the bug.