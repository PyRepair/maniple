### Analysis:
The buggy function `info()` in `fish.py` is attempting to retrieve the version of the Fish Shell by running the command `fish -c 'echo $FISH_VERSION'`. However, the current implementation is not correctly handling the output of the command, leading to an incorrect version string being returned.

The failing test is asserting the output of `shell.info()` to be `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.

The cause of the bug seems to be related to how the function processes the output of the command and constructs the version string.

### Bug Fix Strategy:
1. Update the function to correctly read and parse the version string from the command output.
2. Strip any unnecessary characters or words from the version string before formatting it into the expected output format.

### Corrected Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[-1].strip()
    return u'Fish Shell {}'.format(version)
```

With the above corrected function, it reads the output of the command correctly, strips any unwanted characters or words from the version string, and then formats it into `'Fish Shell version_number'` format for the expected output.

This correction should resolve the failing test and address the issue reported in the GitHub bug post.