### Explanation:
The bug in the `info` function lies in the command used to get the Fish shell version. Currently, the command `echo $FISH_VERSION` is being used to fetch the version, but the correct command should be `fish --version`. This discrepancy is causing the version string to include unnecessary information like "fish, version" leading to the assertion error in the test.

### Fix strategy:
1. Update the command in the `Popen` call to `['fish', '--version']` to properly fetch the Fish shell version.
2. Modify the decoding and formatting of the version string to only extract and use the version number.

### Corrected code:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.replace('fish, version ', '')  # Extract version number from the string
        return f'Fish Shell {version}'
```