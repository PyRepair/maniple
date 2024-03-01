### Analysis:
1. The `info` function in the Fish shell class is supposed to return the name and version of the current shell by running a command in Fish shell and extracting the version. However, the current implementation is not correctly extracting the version information.
2. The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.
3. The runtime values show that the `version` variable is being set to the output of the command without correctly extracting just the version number.
4. To fix the bug, we need to modify how the version number is extracted from the command output.
5. The fix involves parsing the output to extract only the version number without the extra text.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output of the command using `split(', ')` and taking the second part, we can extract just the version number without the extra text. This corrected version should pass the failing test and resolve the issue reported on GitHub.