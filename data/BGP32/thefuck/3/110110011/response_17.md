### Analysis:
1. The buggy function is the `info` method inside the `Fish` class in `thefuck/shells/fish.py`.
2. The test code `test_info` in `tests/shells/test_fish.py` sets up a mock `Popen` object and expects the `shell.info()` method to return 'Fish Shell 3.5.9'.
3. The error message indicates that the actual output of `shell.info()` includes unwanted extra characters ('fish, version') along with the main version number ('3.5.9').
4. The GitHub issue mentions that the `thefuck -v` command hangs due to recursive calls triggered by the `info` method in the `Fish` class, indicating that the incorrect output might be related to incorrect command usage.
5. The issue raised in GitHub also references the fix for this problem.

### Bug Cause:
The bug is caused by passing the wrong command to the `Popen` object in the `Fish.info` method. The expected output is '3.5.9', but the command `echo $FISH_VERSION` returns 'fish, version 3.5.9'.

### Bug Fix Strategy:
To fix the bug, we need to correct the command passed to the `Popen` object in the `Fish.info` method to extract only the version number without any additional text.

### Corrected Version:
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'fish --version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(' ')[-1])
```