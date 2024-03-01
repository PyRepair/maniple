## Bug Explanation
The bug in the `info` function lies in the command used to retrieve the Fish shell version. The command `echo $FISH_VERSION` fetches the `FISH_VERSION` environment variable, but the correct command to get the Fish shell version is `fish --version`. This discrepancy causes the test to fail as the expected version is not obtained.

## Bug Fix Strategy
To fix the bug, we need to change the command executed by Popen to fetch the Fish shell version. Instead of `echo $FISH_VERSION`, we should use `fish --version`.

## Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# The declaration of the class containing the corrected function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(", version ")[1]
        return u'Fish Shell {}'.format(version)
``` 

After applying this fix, the `info` function will correctly retrieve the Fish shell version using the `fish --version` command, allowing the test to pass with the expected version.