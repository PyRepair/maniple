### Explanation:
The bug in the provided function is due to the fact that the version string retrieved from the Popen command includes extra characters (`"fish, version"`) that are not part of the expected version string (`"3.5.9"`). This discrepancy causes the assertion error in the failing test.

The bug revolves around how the version string is extracted from the output of the Popen command. The incorrect extraction results in the extra characters being included in the final output, leading to a mismatch with the expected output.

### Strategy for fixing the bug:
To fix the bug, we need to modify the way the version string is extracted from the output of the Popen command. Specifically, we should extract only the version number part of the output, excluding any additional characters.

### The corrected version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().replace('fish, version ', '')  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By modifying the extraction of the version number and removing the unnecessary characters, the corrected function should now return the expected output and pass the failing test.