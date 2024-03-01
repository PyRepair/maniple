## Analysis
The buggy function `info` is making a call to `Popen` to execute a command in the Fish shell and retrieve the version information. However, the issue arises from the fact that it is trying to read from `stdout` before waiting for the process to complete. This causes the function to return incorrect information or hang in certain cases.

## Bug Cause
1. The use of `proc.stdout.read()` before waiting for the process to complete.
2. Incorrect handling of decoding the output from `stdout`.

## Bug Fix Strategy
1. Use `proc.communicate()` to wait for the process to complete before attempting to read from `stdout`.
2. Properly handle the decoding of the output to ensure correct string representation.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By using `communicate()` after executing the command, we ensure that the process completes before reading from `stdout`, preventing potential hangs or incorrect output. Also, the decoding of the output is properly handled to ensure the correct string representation.