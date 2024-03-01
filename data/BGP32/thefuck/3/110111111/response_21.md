To fix the bug in the `info` function of the `Fish` class, we need to correct the command used to retrieve the Fish shell version. The command should be `fish --version` instead of `echo $FISH_VERSION`. Additionally, we need to adjust the parsing of the output to extract the version number correctly.

Here is the corrected version of the `info` function:

```python
# The declaration of the class containing the fixed function
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[1]
        return u'Fish Shell {}'.format(version)
```

By making these changes, the function will correctly extract the Fish shell version from the output of `fish --version`. This should resolve the failing test and align with the expected input/output values.