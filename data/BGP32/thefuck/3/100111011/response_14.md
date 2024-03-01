### Analysis:
- The buggy function `info` in the `fish.py` file is trying to retrieve the Fish shell version by running a command and capturing the output, but there is a mismatch in the output formatting causing the test to fail.
- The failing test is expecting the version string without any additional text, but the current implementation includes unnecessary text like "fish, version" in the output.
- The `Popen` call is set up incorrectly as it should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to get the version directly.

### Bug Cause:
- The cause of the bug is due to incorrect command execution and the format of the version string being fetched.
- The failing test expects a specific version string format, but the current implementation provides extra text along with the version number.
- The `Popen` call does not fetch the version information as intended, leading to the incorrect version output.

### Fix Strategy:
- Update the `Popen` call to execute `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to get the version directly.
- Modify the version formatting to directly extract the version number without any additional text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

With this corrected version, the function will fetch the Fish shell version correctly and format it without any additional text. This should resolve the failing test and the GitHub issue as well.