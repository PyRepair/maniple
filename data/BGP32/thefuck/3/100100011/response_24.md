## Analysis:
1. The `info` function in the `fish.py` file is supposed to retrieve the version of the Fish shell by executing the command `echo $FISH_VERSION`.
2. The failing test in the `test_fish.py` file sets up a side effect for `Popen` to return the version text `fish, version 3.5.9`.
3. The bug lies in the command being executed by `Popen` in the `info` function, which is using `'echo $FISH_VERSION'` instead of `'fish --version'`.
4. The failing test expects the command `['fish', '--version']` to be used, and this inconsistency causes the test failure.

## Bug Cause:
The bug is caused by the incorrect shell command being used to retrieve the Fish shell version in the `info` function. This discrepancy between the expected shell command in the test and the actual command inside the function leads to the failing test.

## Fix Strategy:
To fix the bug, update the command in the `Popen` call within the `info` function to `['fish', '--version']` to align with the test expectation.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1].strip())
```

Now, the corrected `info` function should correctly obtain the Fish shell version by executing `fish --version` and extract the version number to return 'Fish Shell 3.5.9', resolving the issue reported on GitHub and passing the failing test.