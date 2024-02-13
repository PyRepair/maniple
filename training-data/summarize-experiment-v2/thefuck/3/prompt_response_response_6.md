## Bug Analysis
The bug seems to be related to the incorrect usage of the `Popen` function in the `info` method of the `Fish` class. The failing test indicates that the output of the `info` method is not matching the expected 'Fish Shell 3.5.9' due to incorrect usage of `Popen`. The GitHub issue also provides context that this bug causes a recursive loop in the Oh-My-Fish plugin.

## Bug Cause
The cause of the bug is due to the incorrect usage of the `Popen` function to retrieve the version of the fish shell. The `info` method is not executing the correct command and capturing the actual output, resulting in incorrect values and failing the test.

## Possible Approaches for Fixing the Bug
1. Use the correct command to retrieve the fish shell version using `Popen`.
2. Capture the actual output from the command execution and use it to construct the return value.

## Corrected Function
```python
# The relative path of the buggy file: thefuck/shells/fish.py

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

With this corrected function, the `Popen` function is used correctly to execute the command to retrieve the fish shell version, and the actual output is captured to construct the return value. This code should pass the failing test and resolve the GitHub issue related to the recursive loop in the Oh-My-Fish plugin.