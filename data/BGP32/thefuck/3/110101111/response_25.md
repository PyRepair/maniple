The bug in the `info` function of the `Fish` class is due to the incorrect command used to retrieve the version of Fish shell. The `Popen` command should pass `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']` in order to get the version information correctly.

Here is the corrected version of the `info` function:

```python
# The corrected version of the buggy function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split()[-1]  # Extracting only the version number
        return f'Fish Shell {version}'
```

By updating the `Popen` command to `['fish', '--version']` and making sure to extract only the version number from the output, the `info` function will now correctly retrieve and format the Fish shell version, passing the failing test case and resolving the issue reported on GitHub.