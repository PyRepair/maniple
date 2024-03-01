## Analysis
1. The buggy function `info` in the `Fish` class is attempting to retrieve the version of the Fish shell by running a subprocess command. The returned version is then used to construct a string containing the shell name and version.
2. The error message indicates that the returned version includes extra text ("fish, version") which causes the assertion to fail.
3. The expected behavior is to extract only the version number from the output of the subprocess command and format it into the desired string.
4. To fix the bug, we need to modify the extraction of the version number from the output to remove the unnecessary text.

## Bug Cause
The bug occurs because the output of the subprocess command includes the text "fish, version" along with the version number, which is not expected by the test assertion.

## Fix Strategy
1. Update the code to extract only the relevant version number from the output of the subprocess command.
2. Trim any unnecessary text from the extracted version number before formatting it into the output string.

## Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number without unnecessary text
        version = version.split(' ')[-1]  # Assuming version is the last part separated by space
        return u'Fish Shell {}'.format(version)
``` 

By updating the version extraction logic, the corrected function should now properly extract just the version number from the output and format it into the desired string.