### Analysis:
1. The buggy function `info` in `fish.py` is attempting to retrieve the version of Fish shell using the command `echo $FISH_VERSION`. However, the test case `test_info` is expecting the version to be retrieved using `--version` flag.
2. The error message indicates that the version retrieved by the function does not match the expected version.
3. The GitHub issue mentions that the usage of `thefuck -v` with the plugin triggers a recursive loop due to the incorrect version retrieval method.
4. To fix the bug, we need to modify the command used to retrieve the Fish shell version in the `info` function.

### Fix Strategy:
- Update the command in the `info` function to use `fish --version` instead of `echo $FISH_VERSION` to correctly retrieve the version.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By making this change, the `info` function should now correctly retrieve and return the version of Fish shell using the `--version` flag, which aligns with the expectations of the test case.