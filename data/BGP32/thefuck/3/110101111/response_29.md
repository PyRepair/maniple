The bug in the `info` function of the `Fish` class is related to the fact that the command being executed to retrieve the Fish version (`echo $FISH_VERSION`) is not correctly capturing the version string. The test fails because the expected version string ('3.5.9') is not being extracted from the output of the command.

To fix this bug, we need to change the command executed by the `Popen` instance to obtain the Fish version correctly.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.readline().decode('utf-8').strip()
        version = version.split(', version ')[1]  # Extracting the version string from the output
        return u'Fish Shell {}'.format(version)
```

By changing the command to `['fish', '--version']` and properly extracting the version string from the output, the `info` function should now return the correct version information and pass the failing test case.