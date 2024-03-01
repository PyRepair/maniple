### Bug Analysis:

1. The `info` function in the `Fish` class is supposed to return the name and version of the current Fish shell by executing `fish -c 'echo $FISH_VERSION'`. However, the command being executed in `Popen` is incorrect, it should be `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`.

### Bug Cause:

The bug is caused by the incorrect command being passed to `Popen`. This results in not getting the correct version information from the shell and failing the test.

### Bug Fix Strategy:

To fix the bug, we need to adjust the command passed to `Popen` to `['fish', '--version']` so that the correct version information is obtained from the Fish shell.

### Corrected Version:

```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(',')[1].strip())
``` 

Now, the corrected version of the `info` function will correctly execute `fish --version` to retrieve the version information and return the formatted version string as expected. This fix should address the failing test case and resolve the reported GitHub issue.