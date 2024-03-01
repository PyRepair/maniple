### Analysis
The bug in the `info` function lies in the way it extracts the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. The current implementation includes the shell name `'Fish Shell'` along with the version number, but the expected output only includes the version number without the shell name.

### Bug Cause
The bug is caused by including the `u'Fish Shell '` string in the return value along with the version number extracted from the command output. This results in an incorrect format for the shell name and version display.

### Fix Strategy
To fix the bug, we need to modify the way we construct the return string by removing the `'Fish Shell'` string and only including the version number extracted from the command output.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return version
``` 

By returning only the `version` variable without appending the `'Fish Shell'` string, the function will now correctly display only the version number of the Fish shell.