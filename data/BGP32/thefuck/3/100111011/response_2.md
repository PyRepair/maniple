## Bug Fix Analysis:
1. The `info` function in the `Fish` class is supposed to fetch the version of the Fish shell. However, the command being executed in the `Popen` call is incorrect: `['fish', '-c', 'echo $FISH_VERSION']` instead of `['fish', '--version']`.
2. The failing test asserts the output of `shell.info()` to be `'Fish Shell 3.5.9'`, indicating that the correct version output should match the expected string.
3. The error message shows the actual output being `'Fish Shell fish, version 3.5.9'`, which means the current setup is fetching the incorrect version format.
4. To fix the bug, we need to update the command executed in the `Popen` call to `['fish', '--version']` to get the correct version format.

## Bug Fix Strategy:
1. Update the command being executed by `Popen` to retrieve the Fish shell version correctly.
2. Ensure that the decoded version and the formatting of the output match the expected format.

## Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

In the corrected version, the command executed is changed to `['fish', '--version']`, which retrieves the version of the Fish shell directly. The output is then appropriately formatted to match the expected `Fish Shell X.X.X` format. This fix should resolve the issue reported on GitHub and make the failing test pass successfully.