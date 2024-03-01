## Bug Fix Strategy
1. The current implementation of the `info` function in the `fish.py` file is using the command `echo $FISH_VERSION` to get the Fish shell version, but the test case is expecting the version number to be extracted from the output "fish, version 3.5.9\n". This discrepancy is causing the assertion failure.
2. We need to modify the command used to fetch the Fish shell version in the `info` function to match the expected output format.
3. By updating the command to 'fish --version', we can ensure that the extracted version matches the expected value.

## Corrected Version of the Function

```python
# The relative path of the corrected file: thefuck/shells/fish.py

def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(', version ')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By making the above correction, the `info` function should now correctly extract the Fish shell version in a format that matches the expected output in the failing test case. This will resolve the assertion failure and address the issue reported on GitHub regarding the recursive loop caused by the incorrect version extraction.