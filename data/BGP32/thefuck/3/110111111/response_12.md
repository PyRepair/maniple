To fix the bug, we need to update the command executed to retrieve the Fish Shell version. The current command `echo $FISH_VERSION` is incorrect, it should be `fish --version` instead.

Here is the corrected version of the `info` function in the `Fish` class:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

In this fix:
- We changed the command from `echo $FISH_VERSION` to `fish --version` to correctly retrieve the Fish Shell version.
- We also modified the logic to correctly parse the version from the output of the command.

With this correction, the `info` function should now return the expected output 'Fish Shell 3.5.9' and pass the failing test.