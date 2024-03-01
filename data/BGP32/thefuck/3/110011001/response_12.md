### Analysis
- The error message indicates that the function `info` is returning a string with an unexpected format. Instead of just the version number, it includes extra text.
- The mock values show that the `proc` variable is returning a string with the format `'fish, version 3.5.9'`.
- The function is extracting the version number by using `proc.stdout.read().decode('utf-8').strip()`, which is incorrect in this case since the output includes additional text.

### Bug Cause
The bug is caused by the incorrect parsing of the output from the command `'fish -c echo $FISH_VERSION'`. The function is extracting the version number along with other text, resulting in a mismatch when comparing the expected output.

### Fix Strategy
To fix this bug, we need to modify the way the version number is extracted from the output of the command. We should extract only the version number and remove any additional text before returning it.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
``` 

In the corrected version, the `version` is extracted using the `split` method to separate the text by commas and get the second part, which is the version number. Then, it's stripped to remove any leading or trailing spaces. This should now return the correct version number without any extra text.