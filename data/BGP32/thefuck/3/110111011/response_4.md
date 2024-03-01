### Bug Fix Strategy:
The bug in the `info()` function arises from the incorrect command used to retrieve the Fish shell version. The expected command should be `fish --version` instead of `echo $FISH_VERSION`.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

### Changes Made:
1. Replaced the command argument from `echo $FISH_VERSION` to `--version`.
2. Modified the parsing of the version to extract only the version number after separating by comma.

By making these changes, the `info()` function should now correctly retrieve the Fish shell version and return it in the desired format, resolving the test failure and the GitHub issue related to this bug.