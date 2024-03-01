### Analysis:
1. The buggy function `info` in `fish.py` is supposed to return the name and version of the Fish shell.
2. The failing test `test_info` in `test_fish.py` sets up the `Popen` mock to return a specific version string.
3. The error message indicates that the actual output contains extra text "fish, version" before the version number, leading to the assertion failure.
4. The `Popen` command in the `info` function retrieves the version incorrectly, including unnecessary text.
5. The expected version should only be the version number itself without any extra text.
6. The GitHub issue suggests that the incorrect output can lead to errors when using the plugin with Oh-My-Fish.

### Bug Cause:
The bug is caused by the `Popen` command in the `info` function returning the full string "fish, version 3.5.9" instead of just the version number "3.5.9". This extra text causes the assertion failure in the test.

### Solution:
To fix the bug, we need to extract only the version number from the output of the `Popen` command and return it as the version of the Fish shell.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    full_version = proc.stdout.read().decode('utf-8').strip()
    version = full_version.split(",")[-1].strip()
    return u'Fish Shell {}'.format(version)
```

By modifying the `Popen` command to request `--version` specifically and extracting only the version number from the output, we ensure that the `info` function returns the correct version format expected by the test.