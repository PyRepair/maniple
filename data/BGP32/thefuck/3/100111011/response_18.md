### Explanation:
The bug in the `info` function of the `Fish` class in `fish.py` is caused by the incorrect command used to extract the Fish shell version. In the current implementation, the command `fish -c 'echo $FISH_VERSION'` is being used, which returns a string with additional text (`fish, version X.X.X`). The test is expecting just the version number without any extra text.

### Bug Location:
The bug is located in the line:
```python
version = proc.stdout.read().decode('utf-8').strip()
```
This line is reading the output from the process and is not parsing the version number correctly.

### Bug Cause:
The cause of the bug is that the command `echo $FISH_VERSION` does not return just the version number, but includes additional text (`fish, version X.X.X`). This causes the assertion in the test to fail as it expects only the version number without any extra text.

### Fix Strategy:
To fix the bug, we need to modify the command that is being executed to return only the version number without any additional text.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    parts = version_output.split()
    if len(parts) >= 3:
        version = parts[2]
        return u'Fish Shell {}'.format(version)
    return 'Fish Shell Unknown'
```

In this corrected version, we are using the `fish --version` command to get the version information directly. We then extract the version number from the output and return it in the correct format. This version should pass the failing test and resolve the issue reported on GitHub.