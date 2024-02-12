The issue with the `info` function in the `Fish` class is that it's not correctly reading the version of the Fish shell. It should be using `fish --version` instead of `echo $FISH_VERSION`.

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

This should fix the bug and provide the correct version of the Fish shell. This will also align with the expected input/output variable information provided and resolve the issue posted in GitHub.