The bug in the provided function is caused by the incorrect formatting of the version string. The function is extracting the version info from the output of the command 'echo $FISH_VERSION', which is returning 'fish, version 3.5.9' instead of just the version number '3.5.9'.

To fix the bug, we need to modify the way we extract the version information from the output of the command. We should extract only the version number part and format the return string accordingly.

Here is the corrected version of the function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
        return u'Fish Shell {}'.format(version)
```

With this correction, the function will correctly extract and format the version number, resulting in the expected output 'Fish Shell 3.5.9'.