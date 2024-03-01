### Analysis
The bug is likely caused by the use of `proc.stdout.read()` without waiting for the process to finish, leading to potential issues with reading the output. The value of `proc.stdout.read()` is a MagicMock object, which suggests that the output reading operation might not be working as intended.

### Bug Fix Strategy
To fix the bug, we should wait for the process to finish before reading the output. This can be done by calling `proc.communicate()` after starting the process to ensure that the output is fully available for reading.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.communicate()
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```