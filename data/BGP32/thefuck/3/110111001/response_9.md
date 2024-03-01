### Explanation:
The bug in the `info` function lies in the command used to get the Fish shell version. The command `echo $FISH_VERSION` does not return the version number directly. Instead, it prints `fish, version <version_number>`.

### Fix strategy:
1. Modify the command in the `Popen` call to `fish --version` to get the version number directly.
2. Update the assert statement in the test to compare the expected output with the correct version format.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    version = version.split(", ")[1]  # Extract the version number
    return f'Fish Shell {version}'
``` 

By changing the command to `fish --version` and extracting the version number from the output, the corrected function should pass the failing test.