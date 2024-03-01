### Analysis
1. The buggy function is `info` inside the `Fish` class in the `fish.py` file. It is supposed to return the name and version of the current shell, which is Fish Shell in this case.
2. The error message indicates a failed assertion where the expected output is `'Fish Shell 3.5.9'` but the actual returned value is `'Fish Shell fish, version 3.5.9'`.
3. The failing test provides the information about the `version` variable containing the incorrect string `'fish, version 3.5.9'`.
4. The issue on GitHub suggests that the problem arises when `thefuck -v` hangs Fish Shell initialization due to a recursive loop caused by the `info` function.

### Bug Cause
The bug is caused by the incorrect formatting of the `version` string, which includes additional unwanted characters before the version number.

### Fix Strategy
1. To fix the bug, the `version` string should be properly formatted to extract only the version number from the output of the subprocess command.
2. This can be achieved by splitting the output at the comma and then trimming any leading or trailing whitespace to extract the exact version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

By splitting the `version` string at the comma and selecting the second part, we can extract only the version number and ensure that the correct output is `'Fish Shell 3.5.9'`.