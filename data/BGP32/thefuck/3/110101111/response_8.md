To fix the bug in the `info` method of the `Fish` class, we need to adjust the command used to obtain the version of the Fish shell. The current command `['fish', '-c', 'echo $FISH_VERSION']` does not retrieve the version correctly, resulting in a mismatch between the expected and actual output.

Here's the corrected version of the `info` method:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        proc.stdout.close()
        return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']`, we can retrieve the version of the Fish shell correctly. Additionally, the output is split by spaces so that we can extract the version number accurately. The `proc.stdout.close()` call is added to close the stream after reading the version information.

This corrected version should resolve the issue and pass the failing test case by returning the expected output `'Fish Shell 3.5.9'`.