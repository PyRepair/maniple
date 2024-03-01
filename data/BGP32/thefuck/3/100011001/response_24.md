### Analysis
The `info` function is trying to extract the version of the Fish shell by executing a command using `Popen` and reading the output from the process. However, the extracted version string includes more than just the version number ("fish, version 3.5.9").

### Bug
The bug is caused by the fact that the extracted version string includes unwanted characters ("fish,") along with the version number, leading to a mismatch when comparing with the expected version number.

### Fix
To fix the bug, we need to extract only the version number without any additional characters from the output of the command.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

This corrected version extracts the version number by splitting the output string at the comma and taking the second part (the version number) only. This should now return the correct version number for comparison.