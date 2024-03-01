### Error Location:
The error in the `info` function lies in the command used to extract the Fish shell version. The command `echo $FISH_VERSION` is incorrect; it should be `fish --version` to get the shell's version correctly.

### Bug Explanation:
- The function tries to extract the version of the Fish shell using the command `echo $FISH_VERSION`, which is incorrect.
- The test case sets the expected version as `3.5.9`, but the function returns `fish, version 3.5.9`, indicating that the version extraction is incorrect.
- The GitHub issue mentions a recursive loop due to incorrect version extraction, which confirms the bug.

### Fix Strategy:
Modify the command in the Popen call to `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to correctly fetch the Fish shell version.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.replace('fish, version ', '')  # Extract only the version number
    return u'Fish Shell {}'.format(version)
```

By making this change, the function will correctly extract the version of the Fish shell using `fish --version` and remove the unnecessary text to match the expected version, `'Fish Shell 3.5.9'`. This corrected version should pass the failing test and resolve the issue as reported on GitHub.