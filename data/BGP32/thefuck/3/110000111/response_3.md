Based on the provided information, the bug in the `info` function of the `Fish` class is due to the fact that the `proc.stdout.read()` call is being used directly without waiting for the process to complete. This can cause the function to return before the process has finished, resulting in incorrect or missing output.

To fix the bug, we need to wait for the process to complete before reading from its stdout. This can be achieved by calling `proc.communicate()` after starting the process with `Popen`. This will ensure that the process finishes execution before extracting the output.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By making this change, we ensure that the function correctly waits for the process to complete and retrieve the version information. This corrected version should address the issue reported on GitHub related to Oh-My-Fish's TheFuck plugin causing a recursive loop.