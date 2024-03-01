### Analysis
The `info` function in the `fish.py` file of the `thefuck` repository is supposed to return the name and version of the Fish shell. However, the current implementation is causing a recursive loop when the `thefuck -v` command is used with the Oh-My-Fish plugin. This bug is caused by the function trying to execute `thefuck -v` internally, leading to a loop. The function is meant to simply fetch the Fish shell version using the `echo $FISH_VERSION` command.

### Bug Explanation
The bug is caused by the `info` function internally using `thefuck -v` command to retrieve the Fish shell version when it should be using `echo $FISH_VERSION`. This incorrect command results in a recursive loop when the `thefuck -v` command is invoked, as described in the GitHub issue.

### Bug Fix Strategy
1. Modify the command in the `Popen` call to `echo $FISH_VERSION` to correctly retrieve the Fish shell version.
2. Ensure that the function does not internally call `thefuck -v`.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    version = proc.communicate()[0].decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version, the function uses the correct `echo $FISH_VERSION` command to fetch the Fish shell version, avoiding the recursive loop issue described in the GitHub issue. Now the function should return the correct Fish shell version without causing any loops.