### Potential Error Locations
1. The command used in `Popen` might be incorrect as it should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.
2. The parsing of the version information from the command output might be incorrect.

### Bug Cause
The bug seems to be caused by the incorrect command being executed in `Popen` which does not retrieve the correct version information. This leads to a mismatch between the expected version string and the actual version string extracted from the output.

### Bug Fix Strategy
1. Update the command in `Popen` to retrieve the version by running `['fish', '--version']`.
2. Modify the parsing of the version information from the output to ensure the correct version is captured.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return f'Fish Shell {version.split(",")[1].strip()}'
```

By updating the command in `Popen` to `['fish', '--version']` and parsing the version string correctly, the corrected version of the function should now correctly extract the version information and return the expected result.