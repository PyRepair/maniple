The bug in the provided function `info()` is that it includes the string `'Fish Shell'` when formatting the version number, which is redundant since the version number is already being extracted correctly. Additionally, the function is expected to return only the version number, not the complete version information.

To fix the bug:
1. Remove the string `'Fish Shell'` from the return statement.
2. Update the return statement to only include the version number extracted from the command output.

Here is the corrected version of the function:

```python
    def info(self):
        """Returns the version of the current fish shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return version
``` 

This corrected version should now return only the version number of the fish shell, as expected.