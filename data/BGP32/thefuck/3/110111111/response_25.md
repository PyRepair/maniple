## Addressing the Bug

### Identifying the Issue
The bug in the `info` function of the `Fish` class arises due to incorrect handling of the output obtained from the `fish` command. The function is expected to extract the version number from the output and format it as `'Fish Shell <version>'`. However, the current implementation incorrectly includes the entire output string instead of just the version number. This discrepancy causes the failing test case to raise an assertion error.

### Bug Fix Strategy
To fix the bug, the `info` function needs to correctly parse the version number from the output of the `fish` command and format it as expected. This can be achieved by modifying the `version` extraction logic to isolate the version number within the received string.

### Corrected Function
Here's the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
        return u'Fish Shell {}'.format(version)
```

By using the `split` method with `', version '` as the separator and selecting the last element of the resulting list, we can accurately extract the version number from the output.

### Verification
Once the corrected function is implemented, rerun the failing test case to ensure it no longer raises an assertion error. The provided corrected function should enable the test to pass successfully.

By adopting this solution, the bug causing the failing assertion error in the test case will be fixed, aligning the function's behavior with the expected output.