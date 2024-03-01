The bug in the `info` function is caused by the command used to get the Fish shell version (`echo $FISH_VERSION`) not matching the expected output format (`fish, version 3.5.9`).

### Error:
The `Popen` call uses `['fish', '-c', 'echo $FISH_VERSION']` to retrieve the Fish shell version, but the test expects the version output in the format `fish, version 3.5.9`.

### Strategy for Fixing the Bug:
Modify the command used to retrieve the Fish shell version to match the expected output format in the test.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(', version ')[1])
```

By modifying the command to `['fish', '--version']`, the corrected `info` function will extract the version information in the correct format (`3.5.9`) and pass the failing test.