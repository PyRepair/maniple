### Analysis:
- The `info` function is supposed to retrieve the version of the Fish shell by running the command `echo $FISH_VERSION`.
- The failing test is setting up the `Popen.return_value.stdout.read.side_effect` to return `b'fish, version 3.5.9\n'`.
- The expected output of the `info` function is `'Fish Shell 3.5.9'`, but the actual output includes the extra text `'fish, version'`.
- This discrepancy causes the assertion error in the test.

### Bug:
The bug lies in how the function is parsing the output of the command `echo $FISH_VERSION`. It is not just getting the version number but also including the additional text `'fish, version'`.

### Fix:
To fix the bug, we need to modify the parsing of the output from the command to extract only the version number without any additional text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output based on spaces and taking the last element, we can extract the version number only. This change should address the bug and make the function return just the version number without any extra text.