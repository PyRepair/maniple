### Identified Bug:
The buggy function `info()` in the `fish.py` file is not correctly parsing the output of the `fish -c 'echo $FISH_VERSION'` command. This results in the version string being extracted as `'fish, version 3.5.9'` instead of just `'3.5.9'`. As a result, the assertion in the test fails because the expected version string is `'Fish Shell 3.5.9'` while the actual extracted version string is `'Fish Shell fish, version 3.5.9'`.

### Cause of the Bug:
The bug stems from the incorrect parsing of the output of the `fish -c 'echo $FISH_VERSION'` command. The function is simply returning the full string output of the command without properly extracting just the version number.

### Fix Strategy:
To fix the bug, we need to extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output string at `', '` and selecting the second part, we can isolate the version number. This corrected version of the function should successfully extract the version number and pass the failing test.