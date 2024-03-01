### Bug Explanation:
The bug is causing the assertion to fail because the `info` function is returning the version including the text "fish, version" instead of just the version number itself. This discrepancy results in the assertion error since the expected value does not include the extra text.

### Bug Fix:
To fix the bug, we need to modify the function to extract only the version number from the output of the command `echo $FISH_VERSION`. Since the output includes the text "fish, version" followed by the actual version number, we can split the string and extract the version number.

Here is the corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[-1]  # Extract the version number from the output
    return u'Fish Shell {}'.format(version)
```

This corrected version should now properly extract the version number from the command output and return it in the expected format. The assert statement should pass with this fix.