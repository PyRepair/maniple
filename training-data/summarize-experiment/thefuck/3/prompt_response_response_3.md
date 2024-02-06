The error in the `info` function is caused by the command used to retrieve the Fish shell version. The command `fish -c 'echo $FISH_VERSION'` is incorrect and should be replaced with `fish --version` to get the shell version. Additionally, the mock return value should be set to `'fish, version 3.5.9\n'` instead of just `'3.5.9'`. This will allow the function to correctly parse the version string from the output.

Here's the corrected version of the `info` function:

```python
class Fish(Generic):
    # ... omitted code ...

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

This modified function will now use the correct command to retrieve the Fish shell version and properly parse the version string from the output. This should resolve the issue and allow the function to return the expected version string.