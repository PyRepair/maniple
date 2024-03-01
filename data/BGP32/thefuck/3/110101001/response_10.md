### Bug Analysis
The bug is likely due to the incorrect command being used to get the Fish shell version. The `Popen(['fish', '-c', 'echo $FISH_VERSION'])` command is trying to echo the shell version, but the test is expecting the version to be retrieved using `['fish', '--version']`. Additionally, the handling of the output from the process is incorrect, as it is not properly read and decoded.

### Bug Fix Strategy
1. Update the command in `Popen` to `['fish', '--version']` to retrieve the shell version correctly.
2. Update the way the output is read and decoded to ensure the version is obtained accurately.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
```

The updated version of the `info` function will correctly fetch the Fish shell version using `['fish', '--version']` and extract the version number by splitting the output string and taking the last element.