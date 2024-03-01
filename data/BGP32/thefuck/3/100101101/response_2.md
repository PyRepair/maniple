### Analysis:
- The `info` function is supposed to return the name and version of the current shell by running a subprocess command in Fish shell.
- The bug lies in how the subprocess command is constructed and how the version information is extracted.
- The failing test sets the expected version information to `'3.5.9'`, but the buggy function includes more information like `'fish, version 3.5.9'` which causes the test to fail.

### Bug Cause:
- The bug is caused by the incorrect subprocess command used to retrieve the Fish shell version. The `info` function runs `fish -c 'echo $FISH_VERSION'` which outputs `'fish, version 3.5.9'` instead of just `'3.5.9'`.

### Fix Strategy:
- Modify the subprocess command to extract only the version number without any additional text.

### The corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
``` 

By modifying the subprocess command to `['fish', '--version']` and extracting just the version number without additional text, the corrected function will return `'Fish Shell 3.5.9'` as expected by the failing test.