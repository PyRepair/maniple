### Identified Bug:
The bug in the `info` function is related to how the version of the Fish shell is retrieved. The command `echo $FISH_VERSION` is used to get the Fish shell version, but the expected output format is not matching the actual output format. This results in the assertion error when comparing the shell info with the expected version.

### Cause of the Bug:
The `echo $FISH_VERSION` command returns the version string along with some extra information (`fish, version`). This extra information causes the mismatch between the expected version (`3.5.9`) and the actual version extracted from the command output.

### Fixing the Bug:
To fix this bug, we need to modify how the version is extracted from the command output. We can split the output using `, version` as a delimiter and then extract the version part only.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1]
    return u'Fish Shell {}'.format(version)
```

With this correction, the function should now extract and return only the version part of the shell info, which should match the expected version specified in the test.