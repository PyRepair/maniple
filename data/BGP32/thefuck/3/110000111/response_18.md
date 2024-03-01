## Analysis
The `info` function in the `Fish` class is responsible for returning the name and version of the Fish Shell by executing a command in a subprocess. The issue seems to be related to a recursive loop triggered by the usage of the `thefuck -v` command in the Oh-My-Fish plugin.

## Identified Bug
The bug is likely occurring due to the fact that the `info` function is calling `thefuck -v` command internally, leading to the recursive loop mentioned in the GitHub issue. This causes the function to hang indefinitely.

## Bug Fix Strategy
To fix the bug, it is necessary to modify the `info` function so that it does not call `thefuck -v` command internally, thus breaking the recursive loop.

## Corrected Function
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-v'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

In the corrected version, the `info` function now calls `fish -v` instead of `echo $FISH_VERSION`, which should resolve the recursive loop issue.