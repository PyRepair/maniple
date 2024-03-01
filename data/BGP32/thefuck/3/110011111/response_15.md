### Bug Fix and Corrected Version

#### Bug Explanation:
The bug occurs in the `info` function of the `Fish` class. The `stdout.read()` method returns the entire output at once, including the shell name 'fish,' and 'version'. This leads to the version being extracted as `'fish, version 3.5.9'` instead of just `'3.5.9'`. As a result, the assertion fails since the expected version does not match the actual extracted version.

#### Bug Fix:
To fix this issue, we need to modify the extraction logic for the version. We can split the output by `, version` and only extract the version part. This change will ensure that only the version number is returned, aligning with the expected output.

#### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'fish -v'], stdout=PIPE, stderr=DEVNULL)
        version_output = proc.stdout.read().decode('utf-8').strip()
        version = version_output.split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

By splitting the `version_output` based on `', version '`, we can accurately extract only the version number. This corrected version should resolve the failing test case and align with the expected behavior.