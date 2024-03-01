### Analysis
The bug in the `info` function is caused by the fact that the returned `version` variable still contains the extra text "fish" and a comma before the actual version number. This discrepancy leads to the assertion error when comparing the expected and actual strings.

### Bug Fix Strategy
To fix the bug, we need to modify how the `version` is extracted from the output of the `Popen` command. Instead of just reading the output and stripping it directly, we should extract the version number by splitting the output string and selecting the correct part that represents the version.

### Corrected Version
```python
# The corrected version of the buggy function

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        
        version = output.split(' ')[-1]  # Extract only the version number from the output
        return u'Fish Shell {}'.format(version)
```

After incorporating the fix, the `info` function should return the correct version number '3.5.9' without the extra text 'fish, version' as seen in the failing test, resolving the bug.