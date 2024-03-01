### Identified Bug:
The current implementation of the `info` function in `fish.py` is not correctly parsing the version information obtained from the `echo $FISH_VERSION` command. It results in the version string being prefixed with "fish, version".

### Cause of the Bug:
When the `info` function reads the output from the process, it captures the entire string 'fish, version 3.5.9\n'. However, the expected output is just the version number '3.5.9'. This mismatch causes the assertion failure.

### Fix Strategy:
To fix the bug, we need to modify how the version string is extracted from the output of the process. We should only consider the version number part and discard the unnecessary 'fish, version' prefix.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output on spaces and getting the last element, we extract only the version number. This corrected version should pass the failing test and resolve the issue raised in the GitHub thread.