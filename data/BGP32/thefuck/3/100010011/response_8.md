### Analysis:
The error message indicates that the `info` function in the `fish.py` file is returning the wrong version of the Fish shell. The expected version is 'Fish Shell 3.5.9', but the function is returning 'Fish Shell fish, version 3.5.9'. This discrepancy is causing the test to fail.

### Bug Cause:
The bug is caused by the way the `info` function reads the output of the `echo` command in Fish shell. The function is not properly extracting only the version number from the output, leading to the incorrect format in the return string.

### Bug Fix Strategy:
To fix the bug, we need to properly parse the output of the `echo` command to extract only the version number and then format it correctly in the return string.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

### Explanation:
In the corrected version, we use the `split(',')[1]` operation to extract the version number from the output of the `echo $FISH_VERSION` command. This ensures that we only get the version number without any additional text. Then, we format the version number correctly in the return string.