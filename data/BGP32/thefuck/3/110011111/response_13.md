### Analysis
1. The buggy function `info` in the `Fish` class is intended to get the version of the Fish shell and format it into a specific string.
2. The function is using `Popen` to run the command `fish -c 'echo $FISH_VERSION'` and extract the version from the output.
3. The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output includes extra text.
4. The failing test provides input values for `proc`, `version`, and related variables.
5. The expected values show that only the version number, without extra text, is needed to build the correct output.

### Bug Cause
The issue arises from the fact that the original implementation of extracting the version from the command output didn't properly handle the included text `'fish, version'`.

### Fix Strategy
To fix the bug, we need to modify the code in such a way that only the version number is extracted from the output, without any additional text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(', version')[-1].strip()
        return u'Fish Shell {}'.format(version)
```

By splitting the extracted version using `', version'` as a separator and taking the last part, we can ensure that only the version number is used to generate the final output.