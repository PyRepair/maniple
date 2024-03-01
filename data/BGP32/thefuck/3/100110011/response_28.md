### Analysis:
1. The `info` function is trying to retrieve the Fish Shell version using the command `$FISH_VERSION`, but in the test case, it is expecting the version output from a different command `['fish', '--version']`.
2. This discrepancy leads to the mismatch in the expected and actual version strings, causing the test to fail.
3. The error message clearly shows that the expected version string is missing the prefix `Fish Shell`, indicating that the version retrieval from the command is not as expected.
4. To fix the bug, we need to modify the command used in the `Popen` call to correctly fetch the Fish Shell version.

### Bug Fix Strategy:
1. Modify the command in the `Popen` call to use `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.
2. Update the parsing logic in the `info` function to extract the Fish Shell version correctly from the output of `['fish', '--version']`.

### Updated Corrected Version:
```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    
    version = version_output.split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

Now, with the corrected version of the `info` function, the test should pass successfully, and the issue reported on GitHub regarding the recursive loop should be resolved.