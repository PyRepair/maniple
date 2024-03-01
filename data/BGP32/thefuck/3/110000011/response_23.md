The buggy function `info` in the `Fish` class within the `shells/fish.py` file of `thefuck` tool is causing a recursive loop issue when the `thefuck -v` command is used with Oh-My-Fish plugin. The problem arises from the fact that when `info` function is called with `thefuck -v`, it triggers a call to `fish -c 'echo $FISH_VERSION'` command to retrieve the current Fish shell version. This causes a recursive loop because the `info` function is being called again, resulting in a hang.

To fix this issue, a better approach would be to avoid calling the command `fish -c 'echo $FISH_VERSION'` within the `info` function. Instead, directly access the environment variable `FISH_VERSION` using the `os.environ` module. This way, we can get the Fish shell version without triggering a recursive loop.

Here is the corrected version of the `info` function:

```python
import os

class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        version = os.environ.get('FISH_VERSION', 'Unknown')
        return u'Fish Shell {}'.format(version)
```

By directly accessing the `FISH_VERSION` environment variable, we can avoid the recursive loop issue and ensure that the version information is retrieved correctly without causing the shell initialization to hang.