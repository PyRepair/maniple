The bug in the provided function `info` is caused by the incorrect parsing of the version information obtained from the `fish` shell command. The current implementation tries to extract the version from the output string `'fish, version 3.5.9'`, which includes additional text leading to an incorrect version value.

To fix this bug, we need to modify the parsing logic to extract only the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.

Here is the corrected version of the function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

With this modification, the function will correctly extract the version number from the output string and return it as expected. This solution ensures that the function returns the correct version information of the Fish shell.