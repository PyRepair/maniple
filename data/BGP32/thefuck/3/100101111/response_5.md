## Identification of the bug

The bug in the `info` function lies in the way the version of Fish Shell is being extracted. The command used (`echo $FISH_VERSION`) is not retrieving the correct version information, leading to a mismatch in the expected and actual version string.

The `test_info` function is setting the `Popen.return_value.stdout.read` with a specific version string `b'fish, version 3.5.9\n'`. However, the `info` function is extracting the version from the command output incorrectly, resulting in a version string `'fish, version 3.5.9'` instead of just `'3.5.9'`.

## Cause of the bug

The bug is caused by the incorrect parsing of the version string from the command output in the `info` function. The problem lies in how the version is extracted using `echo $FISH_VERSION`.

## Strategy to fix the bug

To fix the bug, we need to adjust the command used to retrieve the version of Fish Shell so that it only retrieves the version number without any additional text. This can be done by modifying the command used in the `Popen` call.

## The corrected version of the function

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split()[-1]
    return 'Fish Shell {}'.format(version)
```

This corrected version of the `info` function now retrieves the version using the `fish --version` command, extracts just the version number from the output, and returns the correct version string. This modification aligns with the expected version extraction in the failing test.