### Analysis
1. The buggy function `info` is attempting to retrieve the version of the Fish shell by executing a command in a subprocess. It then formats the version string to include in a returned string.
2. The error message shows that the expected output is `'Fish Shell 3.5.9'`, but the actual output contains additional text.
3. The issue points out that the `thefuck -v` command triggers a recursive loop due to the incorrect behavior in `Fish.info()`.
4. To fix the bug, we need to correct how the subprocess output is processed and extract only the version number from it.

### Bug Cause
The buggy function is not correctly extracting the version number from the output of the `fish -c 'echo $FISH_VERSION'` command. It includes additional text like `'fish, version'` in the output, leading to a mismatch with the expected version format.

### Fix Strategy
1. Update the parsing logic to properly extract just the version number from the output string.
2. Strip any unnecessary characters and only keep the version number.
3. Modify the return statement to format the version number correctly.

### Corrected Version
```python
# The corrected version of the buggy function

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```

The corrected version modifies the `version` extraction to split the output by `,` and retrieve the second part, which is the version number. This change ensures that only the version number is returned, matching the expected format `'Fish Shell x.x.x'`.