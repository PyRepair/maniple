## Analysis:
1. The `info` function in the `Fish` class is intended to return the name and version of the Fish Shell.
2. The function uses the `Popen` function to execute a command and retrieve the Fish Shell version. However, the way the output is being handled is causing issues.
3. The bug occurs because the `proc.stdout.read()` method is not returning the output immediately after the command is executed, leading to an empty version string.
4. One strategy to fix this bug is to wait for the process to finish before reading the output.

## Bug Fix:
```python
# The corrected version of the info function
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the process to finish
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By adding `proc.wait()` before reading the output from the process, we ensure that the process completes before trying to read the output. This should fix the bug and correctly retrieve the Fish Shell version.