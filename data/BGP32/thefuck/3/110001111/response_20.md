### Bug Explanation
The bug in the `info` function of the `Fish` class is caused due to the way the `Popen` process is handled. The `proc.stdout.read()` is being called before the process finishes, resulting in the function not getting the correct output version of Fish shell. This leads to the incorrect return value.

### Bug Fix Strategy
To fix this bug, we need to wait for the `Popen` process to finish before reading the output. This can be achieved by calling `proc.wait()` before reading the output.

### Corrected Version of the Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        proc.wait()  # Wait for the process to finish
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

With this correction, the function will properly wait for the `Popen` process to finish before extracting the version information, ensuring the correct output value.