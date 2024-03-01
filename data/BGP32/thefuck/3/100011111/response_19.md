### Bug Analysis
The bug in the `info` function arises from the fact that the `Popen` class object is being used incorrectly. The expected output does not match the actual output due to the incorrect parsing of the version information from the command output. The code is currently appending "Fish Shell" to the entire output of the command, which includes both the shell name and version.

### Bug Location
The bug is located in the line:
```python
version = proc.stdout.read().decode('utf-8').strip()
```
Here, the `version` variable is capturing both the shell name and version as a single string.

### Bug Cause
The cause of the bug is that the code is not properly parsing the version information from the shell command output. It should extract only the version part of the output and not include the shell name.

### Bug Fix Strategy
To fix the bug, the code needs to properly extract and format only the version information from the command output. This can be done by splitting the output based on a delimiter or pattern and then taking the necessary part for the version.

### Corrected Code
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    
    version = output.split(", version ")[-1]
    return u'Fish Shell {}'.format(version)
```

By splitting the output on ", version " and taking the last part, we extract only the version number, which will match the expected output. This corrected code should pass the failing test and provide the expected version information for the Fish shell.