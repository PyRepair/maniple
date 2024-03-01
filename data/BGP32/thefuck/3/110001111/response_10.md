Based on the provided information, the bug in the `info()` function of the `Fish` class is that it is trying to get the version of Fish shell by executing `echo $FISH_VERSION`, but it is not properly capturing the output. This causes issues with the version string and leads to the reported problem on GitHub.

To fix this bug, we need to ensure that the output of the `Popen` command is properly captured and decoded to get the version string. Additionally, we need to trim the version string to remove any extra characters.

Here is the corrected version of the `info()` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.communicate()[0].decode('utf-8').strip()
        version = version.split(',')[-1].strip()  # Get only the version number
        return u'Fish Shell {}'.format(version)
```

With this corrected version, the function will properly capture and decode the output of the `Popen` command to get the version of the Fish shell. It will then trim the version string to extract only the version number, which should resolve the reported issue on GitHub.