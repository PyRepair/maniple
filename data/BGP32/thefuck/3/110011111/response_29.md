### Bug Explanation
The bug in the `info` function is caused by the way the version number is extracted from the output of `fish -c 'echo $FISH_VERSION'`. The expected output is just the version number, but the actual output includes the text "fish, version" prepended to the version number. This discrepancy leads to the assertion failure in the test.

### Bug Fix Strategy
To fix this bug, we need to parse the version number correctly from the output of the `fish -c 'echo $FISH_VERSION'` command. We can achieve this by splitting the output by commas and then taking the last element which represents the version number.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[-1]
        return u'Fish Shell {}'.format(version.strip())
```

By modifying the way we extract the version from the output, the function should now correctly return the version number without any additional text, resolving the test failure issue.