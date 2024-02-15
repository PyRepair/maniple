```python
# The relative path of the buggy file: thefuck/shells/fish.py

from subprocess import Popen, PIPE
from ..utils import DEVNULL, cache

# The fixed version of the function
class Fish(Generic):
    @cache('.fish-shell-version')
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```