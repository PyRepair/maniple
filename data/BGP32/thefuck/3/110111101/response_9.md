### Bug Analysis:
The buggy function `info` in the `Fish` class is intended to return the version of the Fish shell by executing a command. However, the command used to retrieve the version is different from the one provided in the failing test. This leads to a mismatch in the expected and actual output values.

### Bug Location:
The bug is located in the command used in the `Popen` call within the `info` function. The command should be `'fish', '--version'` to match the expected output in the test.

### Bug Explanation:
1. The failing test sets the expectation for the version string to be `'3.5.9'`.
2. However, the function uses the command `'echo $FISH_VERSION'` to get the version instead of `'fish', '--version'`.
3. This results in the `version` variable containing the string `'fish, version 3.5.9'`.
4. When the function formats the output as `'Fish Shell {}'.format(version)`, it includes the unnecessary 'fish, version' part causing the mismatch.

### Bug Fix Strategy:
To fix the bug, update the command in the `Popen` call to `['fish', '--version']` so that the retrieved version matches the expected version in the failing test.

### Corrected Version of the Function:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(', version ')[1])
```

By making this change, the function will execute the correct command to retrieve the version of the Fish shell and format it properly to match the expected output in the failing test.