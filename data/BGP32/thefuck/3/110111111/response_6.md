To fix the bug in the `info` function of the `Fish` class, we need to correct the command that is passed to `Popen`. Currently, the command is `['fish', '-c', 'echo $FISH_VERSION']`, which is not correctly retrieving the Fish shell version.

### Error Analysis:
- The failing test expects the shell version to be extracted by running `echo $FISH_VERSION` in the subprocess, but the expected version is just `'3.5.9'` without any extra text.
- The test mock setup also provides the version without any additional text ('fish, version 3.5.9\n').
- This discrepancy causes the assertion failure due to the difference in the output format.

### Bug Fix Strategy:
- Modify the command passed to `Popen` to directly request the Fish shell version without any extra text.
- Update the function to extract the version correctly based on the modified command.

### Updated Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

The corrected version of the `info` function now directly retrieves the Fish shell version using `['fish', '-v']`, strip any extra whitespaces, and extracts only the version number. This modification aligns the output with the expected format and should pass the failing test.