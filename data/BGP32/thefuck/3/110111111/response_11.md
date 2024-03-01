To fix the bug in the `info` function of the `Fish` class, we need to adjust the command used to retrieve the Fish shell version.

The issue lies in the command used to fetch the shell version. The current command `echo $FISH_VERSION` returns the entire string `fish, version 3.5.9`, including unnecessary text. To fix this, we need to change the command to `fish --version` to directly obtain the version number.

Here is the corrected version of the function:

```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return u'Fish Shell {}'.format(version)
```

By using the `fish --version` command, we directly get the version number without any extra text. Additionally, we split the output to extract only the version number for the comparison.

This fix should resolve the failing test and provide the expected output as per the test case.