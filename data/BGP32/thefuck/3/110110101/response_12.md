### Analysis
1. The `info` function within the `Fish` class is supposed to return the name and version of the current shell (Fish Shell) by executing a command using `Popen`.
2. The failing test is asserting that the `info` function should return 'Fish Shell 3.5.9' but it is failing with an assertion error due to a mismatch in the actual and expected values.
3. The error message indicates that the returned value includes extra text ('fish, version') which is not expected in the output.
4. The cause of the bug is that the command used to retrieve the Fish Shell version is 'echo $FISH_VERSION', but it should have been 'fish --version' to correctly get the version number.
5. To fix the bug, the command passed to `Popen` should be corrected to 'fish --version' to get the correct version number.

### Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

After applying this bug fix, the `info` function will correctly return the version number of the Fish Shell without any extra text, passing the failing test case.