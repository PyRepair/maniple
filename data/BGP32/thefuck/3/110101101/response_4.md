## Analysis
The buggy function `info` in the `Fish` class is trying to retrieve the version of the Fish shell by executing a command `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected output version does not match the actual output. This discrepancy indicates that the command being executed to fetch the version is incorrect.

The failing test provides the expected output version as `'Fish Shell 3.5.9'`, which indicates that only the version number should be extracted from the output of the command.

## Bug Cause
The bug is caused by the incorrect command being executed to retrieve the Fish shell version. The current command `fish -c 'echo $FISH_VERSION'` returns the whole string `'fish, version 3.5.9'`, including extra characters that need to be stripped off.

## Fix Strategy
To fix the bug, the command used to retrieve the version should be modified to only return the version number without any additional text.

## Corrected Version
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
``` 

In the corrected version, the command `fish --version` is used to directly fetch the version without needing to extract or strip any additional characters. The `split()` and `[-1]` operations are applied to retrieve only the version number.