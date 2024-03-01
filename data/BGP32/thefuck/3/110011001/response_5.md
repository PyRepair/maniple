### Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell by executing a command in the shell and then formatting the output into a string. However, the error message indicates that the version retrieved includes extra text that needs to be removed before formatting the final output.

The failing test provides the expected version value without the extra text, indicating that the function is not correctly stripping the unnecessary part when extracting the version.

### Bug Cause
The bug in the current implementation is that the function is not correctly stripping the unnecessary text when reading the output from the subprocess. This causes the output version to include the undesired part, leading to the assertion failure in the test.

### Strategy for Fixing the Bug
To fix the bug, we need to modify the process of retrieving the version from the subprocess output to ensure that only the version number is extracted without any additional text.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version_parts = version.split(',')  # Split the version to remove unnecessary text
        version_number = version_parts[1].strip()  # Get only the version number
        return u'Fish Shell {}'.format(version_number)
``` 

By splitting the version string and extracting the relevant part (the version number) while removing the unnecessary text, the corrected version of the function should now return the expected string without the extra text, passing the test successfully.