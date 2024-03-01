The bug in the current implementation is that the command `echo $FISH_VERSION` is used to get the Fish version, but the actual version output from the command is not being processed correctly. This results in the failing test as the returned version does not match the expected output.

To fix this bug, we need to update the command being executed in the `info` function to `fish --version` which will provide the correct Fish version information.

Here is the corrected version of the function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(',')[1].strip())
```

With this correction, the `info` function will correctly extract the Fish version from the output of `fish --version` command and return it in the expected format.