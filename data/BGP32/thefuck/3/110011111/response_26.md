## Bug Explanation
The bug in the `info` function of the `Fish` class arises because the `version` variable includes the string "fish, version" in addition to the actual version number. However, the comparison in the test expects only the version number without the extra "fish, version" string. This discrepancy causes the assertion error.

## Fix Strategy
To fix the bug, the function needs to extract only the version number from the output and return it in the correct format. The version number can be extracted by splitting the output string and taking the last part after splitting by space and comma. Then the function can return the version number in the expected format.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]
        return u'Fish Shell {}'.format(version)
``` 

With this corrected version, the `info` function should now correctly extract the version number and return it in the expected format, passing the failing test cases.