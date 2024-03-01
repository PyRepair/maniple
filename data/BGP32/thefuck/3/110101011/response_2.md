## Analysis
1. The buggy function `info` in the `Fish` class is attempting to get the version of the Fish shell by executing a command `echo $FISH_VERSION` using `Popen`. However, it is reading the output incorrectly and not matching the expected version format.
   
2. The failing test `test_info` sets up a mock for `Popen` and expects the output of the shell version command to be `'fish, version 3.5.9\n'`. The test then compares this expected version string with the one returned by the `info` function.

3. The issue arises because the `Popen` call is using the command `'echo $FISH_VERSION'` instead of `'fish --version'`, causing the test expectation and the actual output to not match.

4. To fix the bug, the `Popen` command should be changed to `'fish --version'` to correctly get the version of the Fish shell.

## Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
        return u'Fish Shell {}'.format(version)
```

By modifying the command passed to `Popen` to `'fish --version'` and parsing the output string to extract the version number correctly, the bug should be fixed. This fix aligns the function behavior with the expectations of the failing test and resolves the issue reported on GitHub related to the recursive loop in the Oh-My-Fish plugin.