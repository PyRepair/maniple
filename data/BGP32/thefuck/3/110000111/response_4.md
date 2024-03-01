To fix the bug in the `Fish.info()` function, we need to handle the subprocess communication properly and decode the output before returning it. The issue seems to be related to the communication with the subprocess causing a recursive loop in certain scenarios.

To resolve the bug, we should modify the function to read the output of the subprocess correctly and decode it before returning the shell name and version. Here is the corrected version of the function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.readline().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

This corrected version reads a single line of output from the subprocess and decodes it using `utf-8` encoding before returning the shell name and version. This should prevent the recursive loop issue and ensure the correct functioning of the function.