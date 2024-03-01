### Analysis:
1. The `info` function in `fish.py` fetches the version of the Fish shell using the command `echo $FISH_VERSION`. However, the test is expecting the version by running `fish --version`, which causes the test to fail.
2. The test is setting the `Popen` return value to `b'fish, version 3.5.9\n'`, which does not match the output received by the `info` function.
3. The discrepancy between the expected input (`fish --version`) and the actual input (`echo $FISH_VERSION`) causes the test to fail. The test expects the version in a different format than what is being fetched by the function.
4. To fix the bug, we need to update the `info` function to run `fish --version` to fetch the version information in the correct format.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

By updating the command to `['fish', '--version']` in the `info` function, the version information is fetched correctly. Additionally, the `version` string is parsed to extract only the version number. This corrected version should now pass the failing test.