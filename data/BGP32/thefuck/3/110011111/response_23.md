## Bug Explanation

The bug in the `info` function of the `Fish` class arises from incorrectly parsing the output of the `echo $FISH_VERSION` command. The output of the command includes both the literal text "fish, version" and the actual version number. The function directly formats the output without excluding the "fish, version" part, leading to the unexpected string comparison failure in the test.

## Bug Fix Strategy
To fix the bug:
1. Extract the version number from the output of the command by splitting the string and taking the last element.
2. Format the extracted version number into the desired output format.

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

By extracting only the version number from the output of the command and properly formatting it in the return statement, the corrected function will now produce the expected output and pass the failing test.