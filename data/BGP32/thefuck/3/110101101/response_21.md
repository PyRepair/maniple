### Analysis
1. The `info` function in the `Fish` class is intended to return the version of the Fish shell by executing a command.
2. The function uses the `Popen` function to run the command `'fish -c 'echo $FISH_VERSION'` and retrieve the version output.
3. The expected version value is `'3.5.9'`, but the current implementation is not extracting the version correctly from the output.
4. The `Popen` call should use `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` to get the correct version.
5. By modifying the command passed to `Popen`, we can fix the bug and ensure the correct version is extracted.

### Bug Fix
Here is the corrected version of the `info` function:

```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
```

By using `['fish', '--version']` in the `Popen` call, the correct version information will be extracted from the output, and the function should now return the expected version `'3.5.9'`.