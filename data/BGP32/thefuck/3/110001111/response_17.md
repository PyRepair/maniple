### Analysis
1. The buggy function `info()` in the `Fish` class is trying to get the version of the Fish shell by executing a command `'fish -c echo $FISH_VERSION'` using `Popen`.
2. The bug appears to be related to the way the function is reading and decoding the output from the `Popen` process.
3. The issue reported on GitHub suggests that this bug causes a recursive loop when used with Oh-My-Fish plugin.
4. To fix the bug, we need to ensure that the `Popen` process is properly handled and the output is decoded correctly to get the desired version string.

### Bug Fix Strategy
1. Ensure that the `Popen` process is communicated with properly and closed after use.
2. Decode the output of the process to get the version string without extra characters.
3. Update the return value to include only the version string without any additional information.

### Corrected Version
```python
# The relative path of the corrected file: thefuck/shells/fish.py

# Updated Fish class with corrected info() function
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return version
``` 

With this corrected version, the function properly communicates with the `Popen` process, gets the version string from the output, and returns only the version without any additional information. This should resolve the issue reported on GitHub regarding the recursive loop and ensure correct behavior when used with the Oh-My-Fish plugin.