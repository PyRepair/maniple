Based on the error message and the provided code, the bug in the `info` function of the `Fish` class is due to the discrepancy between the expected output ('Fish Shell 3.5.9') and the actual output ('Fish Shell fish, version 3.5.9'). The incorrect value is caused by the way the version is extracted from the command output.

To fix this bug, we need to correct how the version is retrieved from the output of the subprocess. We should modify the portion of code that reads the output to extract only the version number.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return f'Fish Shell {version}'
```

With this modification, the code will extract the last portion of the output (which corresponds to the version number) and format the final string as 'Fish Shell {version}'.

This corrected version should pass the failing test and return the expected output 'Fish Shell 3.5.9'.