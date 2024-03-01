### Analysis:
1. The `info` function is attempting to retrieve the Fish shell version by executing the command `fish -c 'echo $FISH_VERSION'`. However, in the test function, the expected command to retrieve the version is `['fish', '--version']`.
2. The test sets the `Popen` return value to simulate the output of `fish --version`, but the `info` function is trying to read the output of `echo $FISH_VERSION`.
3. Due to the discrepancy in the commands used, the actual output being read by the `info` function does not match the expected output, resulting in the failing assertion error.
4. To fix the bug, we need to modify the `info` function to execute `fish --version` instead of `echo $FISH_VERSION`.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[-1].strip())
```

### Changes Made:
1. Modified the command from `['fish', '-c', 'echo $FISH_VERSION']` to `['fish', '--version']`.
2. Extracted the version number from the output by splitting based on `,` and extracting the last part.

This corrected version should now correctly fetch the Fish shell version using `fish --version` and match the expected output in the failing test.