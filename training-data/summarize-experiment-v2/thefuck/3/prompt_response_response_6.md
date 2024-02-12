The bug in the provided function `info` lies in the command used to retrieve the version of the Fish shell. The command `echo $FISH_VERSION` is incorrect, and should be replaced with `fish --version` to properly retrieve the version.

Here's the corrected code for the `info` function:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

This corrected code for the `info` function should pass the failing test, satisfy the expected input/output variable information, and successfully resolve the issue posted in GitHub.