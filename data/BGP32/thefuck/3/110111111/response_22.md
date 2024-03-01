### Bug Explanation:
The bug in the `info` function of the `Fish` class is caused by the incorrect command used to retrieve the Fish shell version. The `Popen` command is being called with `['fish', '-c', 'echo $FISH_VERSION']` but the expected command should be `['fish', '--version']`. This leads to the version string being extracted incorrectly from the output, causing the mismatch in the test case.

### Bug Fix Strategy:
To fix the bug, we need to modify the `Popen` command to execute `fish --version` instead of `echo $FISH_VERSION`. This will ensure that the correct version string is extracted and formatted correctly.

### Corrected Version of the `info` Function:
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

By making this change, the `info` function will correctly extract the Fish shell version from the output of `fish --version`, leading to the expected output in the failing test case.