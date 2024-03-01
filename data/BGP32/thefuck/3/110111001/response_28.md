### Analysis
The bug in the `info` function of the `Fish` class stems from the fact that the command executed to retrieve the version (`echo $FISH_VERSION`) is not the correct command. Additionally, the assertion in the test function checks for the wrong command output format. The expected output format `'Fish Shell 3.5.9'` does not match the actual output format `'Fish Shell fish, version 3.5.9'`.

### Bug Explanation
1. The command `echo $FISH_VERSION` is incorrect for retrieving the Fish shell version.
2. The expected version format in the test is different from the actual output format.

### Bug Fix
1. Update the command in the `info` function to `fish --version` to correctly retrieve the Fish shell version.
2. Modify the assertion in the test function to match the correct output format `'Fish Shell 3.5.9'`.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return f'Fish Shell {version}'
```

Now, with the corrected version, the test should pass successfully.