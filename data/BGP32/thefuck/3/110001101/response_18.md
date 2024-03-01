### Explanation:
The bug in the provided function is due to the incorrect parsing of the output of the command `echo $FISH_VERSION`. The function is expecting the output to be in the format `fish, version X.X.X`, but it actually returns only the version number `X.X.X`. This discrepancy in the expected output format causes the function to fail.

### Bug Fix Strategy:
To fix the bug, we need to modify the parsing of the command output to extract only the version number without any additional text.

### Corrected Version:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(", version ")[-1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
``` 

By splitting the `version` string on `", version "`, we can extract only the version number without any additional text. This correction ensures that the expected output matches the actual output format.