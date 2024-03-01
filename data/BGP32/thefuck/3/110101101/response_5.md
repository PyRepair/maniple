### Analysis:
1. The `info()` function is trying to get the Fish shell version by executing the command `fish -c 'echo $FISH_VERSION'`. However, in the failing test, the expected command is `fish --version`.
2. The function is currently extracting the version by reading the output and stripping it, which seems correct.
3. The failing test is asserting the output with the expected string 'Fish Shell 3.5.9'. The test fails because the version extracted from the command output is not matching the expected value.
4. The strategy for fixing the bug is to update the command being executed in the `Popen()` call to `'fish --version'` instead of `'fish -c 'echo $FISH_VERSION'`.
5. Here is the corrected version of the `info()` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split()[-1])
``` 

This corrected version will execute the correct command to get the Fish shell version and extract the version information correctly for comparison with the expected output.