## Analysis
1. The buggy function `info()` is trying to get the version of the Fish shell by executing `fish -c 'echo $FISH_VERSION'`. However, it should be executing `fish --version` based on the test case assertion.
2. The test is mocking the output of `fish --version` but the function is reading `FISH_VERSION` environment variable instead.
3. The function is incorrectly trying to read the `FISH_VERSION` environment variable instead of parsing the version output from `fish --version`.
4. We need to modify the command passed to `Popen` to execute `fish --version` to get the correct shell version.

## Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']` and extracting the version from the output instead of trying to read an environment variable, we can fix the bug.