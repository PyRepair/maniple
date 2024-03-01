## Analysis:
1. The `info` function is intended to fetch the version of the fish shell, but the command used to retrieve the version (`echo $FISH_VERSION`) may not always provide the desired output.
2. The failing test asserts that the function should return `'Fish Shell 3.5.9'`, but the actual output includes extra text "fish, version".
3. The error message clearly shows the mismatch between the expected output and the actual output from the `info` function.
4. To fix this, we need to modify the command executed by the `Popen` call in the `info` function to ensure it correctly retrieves the fish shell version.
5. One possible strategy for fixing the bug is to change the command to `['fish', '--version']` instead of just `'echo $FISH_VERSION'` to get the correct version information.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version_info = version.split(', ')[1]  # Extracting the version number
    return u'Fish Shell {}'.format(version_info)
```

With this corrected version, the `info` function should correctly fetch the fish shell version when tested.