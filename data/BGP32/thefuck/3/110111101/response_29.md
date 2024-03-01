### Bug Explanation
The bug in the `info` function of the `Fish` class arises from two main issues:
1. The command used to fetch the Fish shell version is incorrect. It should be using `fish --version` instead of `echo $FISH_VERSION`.
2. The comparison in the test is failing because the version returned includes additional text "fish, version" which is not expected.

### Bug Fix Strategy
To fix the bug, we need to:
1. Update the command in the `Popen` call to `fish --version`.
2. Strip the unnecessary text "fish, version" from the version string before formatting it in the return statement.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')
        return u'Fish Shell {}'.format(version)
```

After applying the corrected version of the function, it should correctly fetch the Fish shell version using `fish --version` command and return the expected string `'Fish Shell 3.5.9'`.