### Analysis:
The issue in the `info` function arises from the mismatch in the expected version format and the actual version format returned by the `fish -c 'echo $FISH_VERSION'` command. The expected version is "3.5.9" but the actual version returned includes the text "fish, version" before the version number.

### Bug:
The `info` function does not extract the version number correctly and includes additional text in the output, leading to a version mismatch.

### Strategy for fixing the bug:
1. Modify the command to extract the version number without additional text.
2. Update the assertion in the failing test to match the exact format of the version number.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
```

By using `['fish', '--version']` as the command, we ensure that only the version number is returned without any additional text. Additionally, we modify the return statement to extract the version number correctly from the output.

With these changes, the corrected version of the function should now pass the failing test.