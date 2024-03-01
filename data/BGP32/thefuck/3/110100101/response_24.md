## Analysis
The buggy function `info` in the `Fish` class is using the wrong command (`'echo $FISH_VERSION'`) to get the Fish shell version. Additionally, the test is expecting the shell version output in a different format (`'fish, version 3.5.9\n'`) than what is actually being returned by the command.

## Bug cause
1. The command used to get the Fish shell version is incorrect.
2. The format of the shell version output does not match the test expectation.

## Fix strategy
1. Update the command used by `Popen` to retrieve the Fish shell version.
2. Update the format of the shell version output to match the test expectation.

## Corrected version of the function
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]
        return u'Fish Shell {}'.format(version)
```

By making the above modifications, the corrected function should now return the correct Fish shell version and pass the failing test case.