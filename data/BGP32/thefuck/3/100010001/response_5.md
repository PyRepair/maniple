### Analysis:
The error message indicates that there is a discrepancy between the expected output and the actual output of the `info` function in the Fish shell. The expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`.

### Identified Issue:
The issue lies in the way the version information is extracted from the output of the `echo $FISH_VERSION` command in the `info` function. The version information contains additional text `'fish, version'` before the actual version number, which causes the discrepancy.

### Bug Fix Strategy:
To fix this bug, we need to modify the way we extract the version number from the output of the `echo $FISH_VERSION` command. We should only extract the version number itself without any additional text.

### Corrected Version:
```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version_number = version_output.split(', ')[-1]
    return u'Fish Shell {}'.format(version_number)
```

In the corrected version above, we extract just the version number by splitting the `version_output` based on the `', '` delimiter and taking the last element of the resulting list. This ensures that only the version number is returned without any additional text, resolving the bug.