### Bug Explanation

The bug in the `info` function in the `Fish` class is caused by the incorrect command used to fetch the Fish shell version. The current command `['fish', '-c', 'echo $FISH_VERSION']` returns the output in a format that includes the text "fish, version" followed by the actual version number, resulting in a mismatch during comparison in the test function.

Additionally, the referenced GitHub issue indicates that the `info` function triggers a recursive loop when `thefuck -v` is used due to incorrect command execution.

### Bug Fix Strategy

To fix this bug, we need to update the command used to retrieve the Fish shell version to match the expected version format in the test cases. We should ensure that the command executed matches the desired output format "3.5.9" without any extra text.

### Corrected Function

Here is the corrected version of the `info` function:

```python
# The corrected version of the info function in fish.py
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By modifying the command to `['fish', '--version']` and extracting the last element of the split version string, we ensure that the retrieved version matches the expected format for comparison in the test cases.

This corrected version should pass the failing test and resolve the issue mentioned on GitHub.