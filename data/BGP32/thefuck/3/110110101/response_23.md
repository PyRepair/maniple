### Analysis
- The `info` function in the `Fish` class makes a call to the Fish shell to retrieve the version using the command `echo $FISH_VERSION`.
- The failing test case is checking if the expected output of the `info` function matches the actual output from the shell command.
- The error message indicates that the expected output includes unwanted extra text ("fish, version") which is causing the assertion to fail.

### Bug
The bug in the original function is caused by the incorrect shell command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` returns additional information ("fish, version x.y.z") along with the version number.

### Fix
To fix the bug, the shell command needs to be modified to retrieve only the version number without the extra text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(",")[1].strip()
        return u'Fish Shell {}'.format(version)
```

With this correction, the `--version` flag is used to retrieve only the version number from the Fish shell, and any extra text is removed by splitting the result. This will ensure that the function returns the expected output and passes the failing test.