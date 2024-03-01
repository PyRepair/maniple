### Bug Explanation
The bug in the `info` function arises from the command used to retrieve the fish shell version. The command `echo $FISH_VERSION` only prints "fish, version 3.5.9" without just the version number. This causes the comparison in the test to fail because the expected output is simply the version number.

### Bug Fix Strategy
To fix the bug, we need to modify the command used to obtain the shell version to only output the version number without any additional text.

### Corrected Version of the Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'fish --version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(",")[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

By modifying the command to `fish --version`, it will output only the version number. Additionally, splitting the output by the comma and getting the second part will extract just the version number.