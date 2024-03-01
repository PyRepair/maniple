### Explanation:
The bug in the code is due to the incorrect parsing of the version information returned by the `fish` shell. The current implementation reads the output as a whole string and includes unnecessary text like "fish, version" in the version number.

### Bug Fix Strategy:
To fix the bug, we need to modify the code to properly extract and format the version number from the output of the `fish` shell command.

### Corrected Version:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return f'Fish Shell {version}'
``` 

By splitting the output from the `fish --version` command and only keeping the version number, we can fix the bug and ensure that the function returns the correct version information.