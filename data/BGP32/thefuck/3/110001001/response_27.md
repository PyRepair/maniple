### Analysis
The bug in the `info` function lies in how the stdout of the process created by `Popen` is being read. The `read` method is being called directly on `proc.stdout`, which is a `MagicMock` object instead of the actual stream of data from the process.

### Bug Cause
The bug is caused by not properly handling the stdout stream of the process created by `Popen`. Instead of reading from the stream, the `read` method is being called on a MagicMock object, which does not contain the actual output from the `echo $FISH_VERSION` command.

### Fix
To fix this bug, we need to correctly read the data from the stdout stream of the process. We can achieve this by using the `communicate` method of the `Popen` object, which will wait for the process to finish and return both the stdout and stderr streams.

### Corrected Version
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

With this correction, the `communicate` method is used to capture the stdout stream data correctly, which should fix the bug.