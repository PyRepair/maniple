### Explanation:
The bug in the provided function is that the version obtained from the `echo $FISH_VERSION` command includes extra text "fish, version". This extra text is not expected in the final output "Fish Shell 3.5.9", causing the assertion error.

The issue arises from the fact that the output of `proc.stdout.read().decode('utf-8').strip()` contains the extra text "fish, version". This is due to the `echo $FISH_VERSION` command outputting the full version string including the unnecessary information.

### Fix strategy:
To fix the bug, we need to extract only the version number from the output of the `echo $FISH_VERSION` command. In this case, we can split the obtained version string based on spaces and select the last part which represents the version number.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(' ')[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the version string obtained from the command and selecting only the last part, we ensure that only the version number is used in the final output "Fish Shell 3.5.9". This corrected version should pass the failing test with the expected output.