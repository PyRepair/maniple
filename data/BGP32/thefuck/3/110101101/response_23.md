## Analysis
1. The `info` function is trying to fetch the version of the Fish shell by running the command `echo $FISH_VERSION` and capturing the output. 
2. The failing test sets up the mocked stdout with the value `b'fish, version 3.5.9\n'`, but the function is expecting only the version number without the extra text.
3. The function is currently using the wrong command to fetch the version and is not processing the output correctly.
4. To fix the bug, we need to change the command to `fish --version` and extract only the version number from the output.

## Bug Fix
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

By changing the command to `fish --version` and extracting the version number correctly, the bug should be fixed and the function should now return the expected output `Fish Shell 3.5.9`.