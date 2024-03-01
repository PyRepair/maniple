Based on the code provided, the buggy function `info` in the `Fish` class fails to correctly extract the version information from Fish shell, leading to a comparison failure in the test case. The key issue is that the command being executed in the Popen call is incorrect, causing the version string to include unnecessary information.

### Error Cause:
- The incorrect command 'fish -c echo $FISH_VERSION' is used to retrieve the Fish shell version.
- The variable `version` contains the complete output string that includes unnecessary information.

### Strategy for Fixing the Bug:
- Modify the command in the Popen call to obtain only the version information.
- Update the extraction of the version string to include only the version number.

### Corrected Version of the Buggy Function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', version ')[-1]
        return u'Fish Shell {}'.format(version)
```

With this corrected version of the function, it will correctly fetch the Fish shell version using the `--version` command and extract only the version number, passing the failing test case as expected.