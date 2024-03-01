### Analysis
The buggy function is attempting to retrieve the version of the Fish shell by executing the command `echo $FISH_VERSION` using `Popen`. The issue arises due to the fact that the output of the command includes extra text (`'fish, version '`) that needs to be removed to match the expected output. The function is not properly parsing the version number from the command output.

### Bug Explanation
The `version` variable in the buggy function holds the entire output of the command, including the `'fish, version '` prefix, which leads to a mismatch with the expected output. The function needs to extract only the version number from the command output to ensure the correct comparison.

### Bug Fix Strategy
To fix the bug, we need to modify the process of retrieving the version number from the command output. This can be achieved by splitting the obtained string based on the separator `', version '`, and then taking the second part as the version number.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the obtained output based on `', version '`, we extract only the version number. This corrected version of the function should now correctly return `'Fish Shell 3.5.9'`, matching the expected output.