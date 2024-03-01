## Analysis:
1. The `info` function is supposed to return the name and version of the current shell, in this case, the Fish shell.
2. The bug seems to be related to the command used to extract the Fish shell version.
3. The failing test provides the expected version output but the command used to retrieve the version does not match with the command used in the test.
4. The `Popen` call in the `info` function needs to be corrected to match the command expected in the test.
5. We need to change the command from `echo $FISH_VERSION` to `fish --version` to accurately retrieve the Fish shell version.

## Correction:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
```

With this correction, the `info` function will execute the correct command to retrieve the Fish shell version, and it should now pass the failing test.