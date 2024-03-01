### Analysis
1. The buggy function `info` in `fish.py` is failing the test because it is expecting the version output to be in the format of `'Fish Shell 3.5.9'` but the actual output is `'fish, version 3.5.9'`.
2. The cause of the bug lies in how the `version` variable is extracted from the output of the `Popen` command in the `info` function.
3. The failing test is asserting `'Fish Shell fish, version 3.5.9' == 'Fish Shell 3.5.9'`, indicating that the actual output includes extra characters ('fish, version') compared to the expected output.
4. To fix the bug, we need to modify the way the `version` variable is extracted to only include the version number without the additional characters.
5. The corrected version should only return the version number without any extra characters.

### Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this bug fix, the `info` function will correctly extract the version number without any additional characters, and the test should now pass successfully.