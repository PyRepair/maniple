### Analysis:
1. The `info` function is attempting to retrieve the Fish shell version by running the command `fish -c 'echo $FISH_VERSION'` and extracting the version from the output.
2. The failing test sets up the `Popen` mock to return `b'fish, version 3.5.9\n'`, but the function is extracting the version incorrectly, resulting in the extra text "fish, version" in the version string.
3. The bug is causing the extracted version to include unnecessary text, leading to the assertion failure in the test.
4. To fix the bug, we need to modify the way the function extracts the version from the output to only retrieve the version number itself.
5. The corrected version of the function should strip out unnecessary text to return just the version number.

### Bug Fix:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_info = proc.stdout.read().decode('utf-8').strip()
    version = version_info.split()[-1]
    return u'Fish Shell {}'.format(version)
```

By modifying the `Popen` command to use `['fish', '--version']` directly, we can extract the version number more accurately by splitting the output based on whitespace and taking the last part. This corrected version should now pass the failing test.