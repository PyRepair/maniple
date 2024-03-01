The bug in the provided function is that it is not correctly extracting the version number from the output of the command `echo $FISH_VERSION`. The function is currently returning the complete string with "Fish Shell" prefix included.

### Cause of the bug:
The bug is likely in the line where the version number is extracted from the output of the `echo $FISH_VERSION` command. The function is not correctly parsing the output to extract just the version number.

### Strategy to fix the bug:
To fix the bug, we need to modify the extraction process to only capture the version number from the output of the command.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    if version.startswith('fish, version '):
        version = version[len('fish, version '):]
    return version
```

This corrected version of the function will extract the version number correctly and return only the version number without the "Fish Shell" prefix. This should satisfy the expected input/output values provided.