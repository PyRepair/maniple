### Explanation
The bug in the provided function lies in how the `Popen` object is being used. The `Popen` function returns a `subprocess.Popen` object, which represents the running process. When trying to read the output of the process using `proc.stdout.read()`, it results in an empty string because the output has already been read. This leads to the `version` variable being an empty string instead of the expected version number.

### Strategy for fixing the bug
To fix this bug, we need to wait for the process to finish and then read the output. We can achieve this by calling the `communicate()` method on the `Popen` object, which will wait for the process to finish before reading the output.

### Corrected version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

This corrected version ensures that the output of the process is read correctly by calling `proc.communicate()` before decoding the output to get the version.