Based on the provided information, the issue seems to be with the `Fish.info()` function in the `fish.py` file of the `thefuck` project. The function is attempting to retrieve the Fish shell version by executing a command, but it is not extracting the version properly, leading to issues related to the Oh-My-Fish plugin.

The bug occurs because the function reads the entire output of the command as a single string and includes unnecessary text like `'fish, version'` in addition to the version number. To fix this bug, the output needs to be parsed to extract only the version number.

To correct the bug, the function should be updated as follows:

```python
from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]  # Extract only the version number
        return u'Fish Shell {}'.format(version)
```

By splitting the retrieved version string with `split(', ')`, we can extract only the version number without any unnecessary text. This should resolve the issue raised in the GitHub report and provide the expected output.