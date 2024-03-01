### Analysis
- The `info` function in the `Fish` class is attempting to retrieve the Fish shell version using a subprocess call to `fish -c 'echo $FISH_VERSION'`.
- The failing test is designed to check if the function correctly extracts the version number from the output.
- The test is failing because the function is not parsing the version number correctly from the subprocess output.
- The current implementation is extracting the entire output string "fish, version 3.5.9", which includes unnecessary text.

### Bug Fix Strategy
- The bug seems to be related to how the function is extracting the version number from the subprocess output.
- To fix the bug, we need to adjust the way we read and extract the version number to only store "3.5.9" without any additional text.

### Corrected Version
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()  # Read the output
        version = version.split(' ')[-1]  # Extract the version number
        return f'Fish Shell {version}'
```

The corrected version adds an extra step to extract only the version number from the subprocess output. This change should address the bug and make the function return the expected output.