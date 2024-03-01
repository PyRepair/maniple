## Analysis:
1. The `info` function in the `Fish` class is trying to get the version of the Fish shell by executing a command using `Popen`. 
2. The error message indicates that the returned output from the subprocess contains more than just the version number, causing the assertion to fail.
3. The bug is caused by the fact that the `Popen` process is reading the output as a byte string (`b'fish, version 3.5.9\n'`), and then trying to decode it to a string, which results in additional characters being included in the output.
4. To fix the bug, we need to properly decode the output of the subprocess and extract only the version number before returning it.

## Correction:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[-1].strip()  # Extract version only
        return u'Fish Shell {}'.format(version.strip())
``` 

With this correction, the function will extract only the version number from the output of the subprocess, ensuring that it matches the expected format when compared in the test.