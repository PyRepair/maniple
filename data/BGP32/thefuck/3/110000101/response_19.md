### Analysis
The bug in the given function lies in how the `stdout` of the subprocess `proc` is being read. The code tries to directly read from `proc.stdout`, but it should be using the `communicate()` method of the `Popen` object to properly read the output.

### Bug Explanation
The bug occurs because the `stdout` of the `Popen` object is not being read correctly. Directly calling `proc.stdout.read()` may result in the buffer not being ready or closed, leading to an empty or incorrect output.

### Fix Strategy
The correct way to read the output of a subprocess in Python is by using the `communicate()` method on the `Popen` object. This method waits for the process to finish and returns a tuple of `(stdout_data, stderr_data)`. By using this method, we can ensure that the output is read correctly.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)

        stdout_data, _ = proc.communicate()
        version = stdout_data.decode('utf-8').strip()

        return u'Fish Shell {}'.format(version)
```