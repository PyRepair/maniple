To fix the bug in the `info` function of the `Fish` class, we need to update the command sent to the subprocess `Popen` to request the Fish version correctly. The current command is `['fish', '-c', 'echo $FISH_VERSION']`, but it should be `['fish', '--version']` based on the test information provided.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

This corrected version of the function will now correctly retrieve the Fish version information, ensuring that the function behaves as expected in the failing test case.