### Analysis:
1. The `info` function in the `Fish` class is supposed to return the name and version of the current shell by executing a command in the Fish shell.
2. The function uses `Popen` to run the command `fish -c 'echo $FISH_VERSION'` to get the Fish shell version.
3. The failing test function expects the version string returned by the command to be 'Fish Shell 3.5.9'.

### Identified Issue:
The command executed in the `Popen` call is incorrect. Instead of `'fish -c 'echo $FISH_VERSION'`, it should be `'fish --version'` to get the correct version string.

### Bug Cause:
The bug is caused because the command used in the `Popen` call does not retrieve the version string correctly, leading to a mismatch with the expected result in the test.

### Fix Strategy:
Change the command in the `Popen` call from `['fish', '-c', 'echo $FISH_VERSION']` to `['fish', '--version']` to fetch the version string correctly.

### Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        raw_output = proc.stdout.read().decode('utf-8').strip()
        version = raw_output.split()[2]  # Extracting version from the output
        return u'Fish Shell {}'.format(version)
``` 

Now, the corrected version of the `info` function should pass the failing test.