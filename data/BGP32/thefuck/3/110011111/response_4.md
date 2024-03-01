## Identify the bug
The bug in the `info` function of the `Fish` class is related to how it retrieves the shell version from the output of the `fish -c 'echo $FISH_VERSION'` command. The extracted version includes the unnecessary `fish,` prefix, causing the assertion to fail.

## Error Cause
The error stems from the fact that the command `fish -c 'echo $FISH_VERSION'` returns the output in a format that includes the word `fish,` along with the actual version number. This extra part is not necessary and causes the comparison in the test to fail.

## Fix Strategy
To fix the bug, we need to modify the way we extract the version number from the command output so that it only includes the actual version number without any unnecessary prefixes.

## Corrected Version

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By splitting the output and taking only the last part after the comma, we ensure that only the version number is included in the `version` variable. This corrected version should now pass the failing test and provide the expected output.