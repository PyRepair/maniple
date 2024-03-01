### Steps to fix the bug:

1. **Analysis**:
   - The buggy function `info` is attempting to retrieve the version of Fish shell using the command `echo $FISH_VERSION`.
   - The error message shows that the actual output includes extra text (`fish, version`) which is not expected.
   - The test case is failing due to a mismatch in the expected and actual output version of Fish shell.
   - The GitHub issue indicates that this issue is related to the initialization of Fish shell with the Oh-My-Fish plugin.

2. **Identify potential error locations**:
   - The issue seems to be with how the version text is being parsed from the command output.

3. **Explanation of the bug**:
   - The bug is caused by the incorrect parsing of the Fish shell version from the command output. The version text is not being extracted properly, leading to extra characters in the output string.

4. **Suggested strategy for fixing the bug**:
   - Modify the way the version is extracted from the command output to ensure only the version number is included in the final result.

5. **Corrected version** of the `info` function:

```python
# The declaration of the class containing the corrected function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extract only the version number from the output
        version = version.replace('fish, version ', '')  # Remove 'fish, version' prefix
        
        return u'Fish Shell {}'.format(version)
```

With this correction, only the version number will be extracted from the output, leading to the expected version string 'Fish Shell 3.5.9'.