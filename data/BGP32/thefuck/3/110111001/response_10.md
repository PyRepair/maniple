### Explanation of the bug:
The bug in the `info` function seems to be related to the command used to retrieve the Fish shell version. The command `'echo $FISH_VERSION'` returns `'fish, version 3.5.9\n'`, including the extra text `'fish, '`. This extra text causes a mismatch in the returned version string, causing the test to fail.

### Bug Fix Strategy:
To fix this bug, we need to modify the command used to retrieve the Fish shell version so that it only returns the version without any additional text.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'fish --version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By modifying the command passed to `Popen` to `'fish --version'`, we ensure that the output contains only the version number, allowing the function to return the correct version string.