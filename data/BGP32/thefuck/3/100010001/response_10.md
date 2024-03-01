## Analysis
1. The `info` function attempts to get the version of the Fish shell by executing a command and capturing its output.
2. The error message indicates that the captured version includes additional text (`fish, version`) that is not expected in the final output.
3. The bug causes the returned version to be incorrectly formatted, resulting in the assertion failure.
4. To fix the bug, we need to remove the extra text (`fish, version`) from the captured version.

## Bug Fix
To fix the bug, we need to modify the way we retrieve the version from the command output. We should only extract the version number and discard any additional surrounding text. Here's the corrected version of the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number from the output
    version = version.replace('fish, version ', '')
    return 'Fish Shell {}'.format(version)
```

By replacing the prefix `fish, version` with an empty string from the extracted version, we ensure that only the version number is included in the final output. This correction should resolve the bug and allow the test to pass successfully.