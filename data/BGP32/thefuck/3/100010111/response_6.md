## Analysis
1. The buggy function `info` is trying to get the version of the Fish shell by executing a command and reading the output. However, the issue lies in how the output is being read and formatted.
2. The error message indicates that the version obtained includes extra information before the actual version number, leading to a failed assertion.
3. The expected output should only contain the version number without any preceding text.
4. To fix this bug, we need to correctly extract only the version number from the output of the command.
5. By modifying the way the version is extracted, we can ensure that the output matches the expected format.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    # Extract only the version number from the output
    version = version.strip('fish, version ').split('\n')[0].strip()
    return u'Fish Shell {}'.format(version)
```

By modifying the extraction of the version number from the output, we can ensure that only the version number is included in the returned string. This should fix the bug and make the function return the expected output.