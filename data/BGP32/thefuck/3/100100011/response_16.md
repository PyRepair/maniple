## Analysis:
1. The `info` function in `fish.py` is supposed to return the name and version of the Fish shell by executing the command `"fish -c 'echo $FISH_VERSION'"`.
2. The test case `test_info` in `test_fish.py` sets up a mock behavior for `Popen` to return the output of `fish --version`.
3. The bug appears to be caused by the mismatch between the command being executed in the `info` function and the expected output in the test case.
4. The GitHub issue suggests that `thefuck -v` hangs Fish shell initialization due to a recursive loop, indicating a potential problem with the command used in the `info` function.

## Bug Cause:
The bug is caused by the mismatch between the command called by `Popen` in the `info` function and the expected command output set in the test case. The `info` function is executing `"fish -c 'echo $FISH_VERSION'"`, while the test case expects the version output of `fish --version`.

## Fix Strategy:
1. Update the command in the `info` function to match the expected output in the test case.
2. Modify the `info` function to run `"fish --version"` to match the expected version output set in the test case.
3. Update any relevant assertions in the test case to ensure they correspond to the modified command and expected output.

## Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.replace('fish, version ', ''))  # Extract version from output

```

With this correction, the `info` function now calls `"fish --version"` to get the shell version. Additionally, the function extracts the version from the output by removing the leading text "fish, version " before formatting it accordingly. The corrected version should now correctly return the version as expected by the test case.