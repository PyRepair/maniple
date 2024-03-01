### Analysis
The bug occurs in the Fish shell implementation within the `info` method. The issue seems to be related to the recursive loop triggered by using `thefuck -v` in combination with the `Oh-My-Fish` plugin. The current implementation does not handle this scenario correctly, leading to a hang in the Fish shell initialization.

### Bug Identification
The bug is likely caused by the recursive loop that is triggered when invoking `thefuck -v` with the `Oh-My-Fish` plugin, leading to unexpected behavior in the `info` method. The code attempts to retrieve the version of the Fish shell without checking for this specific scenario, resulting in the hang.

### Bug Fix Strategy
To fix the bug, we need to modify the `info` method to handle the case when `thefuck -v` is invoked with the `Oh-My-Fish` plugin more gracefully. One potential solution is to check for the specific combination of commands and provide a different response or prevent the recursive loop from occurring.

### Corrected Version
Below is the corrected version of the `info` method that takes into account the scenario described in the GitHub issue:

```python
def info(self):
    """Returns the name and version of the current shell"""
    cmd = ['fish', '-c', 'echo $FISH_VERSION']
    if '-v' in cmd:
        return "Fish Shell - Version check requested, skipping"
    
    proc = Popen(cmd, stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version, if the command contains `-v`, the method returns a message stating that a version check was requested, skipping the version retrieval process. This adjustment should prevent the recursive loop issue described in the GitHub problem.