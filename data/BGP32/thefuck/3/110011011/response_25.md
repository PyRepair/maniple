### Fixing the Bug

#### 1. Analyze:
- The buggy function `info()` in the `Fish` class is trying to retrieve the version of the Fish shell, but the way it extracts and formats the version is leading to an error.
- The failing test indicates that the expected output is `'Fish Shell 3.5.9'`, while the actual output is `'Fish Shell fish, version 3.5.9'`.
- The GitHub issue suggests that there might be an issue with Oh-My-Fish's TheFuck plugin interacting with this function.

#### 2. Potential Error Location:
The issue seems to be with how the version information is extracted and formatted from the output of the command.

#### 3. Bug Cause:
The bug is caused by the incorrect parsing and formatting of the shell version retrieved from the command output in the `info()` function.

#### 4. Strategy for Fixing:
To fix the bug, we need to extract only the version number from the output of the command and correctly format it as `'Fish Shell {version}'`.

#### 5. Corrected Version:
Here is the corrected version of the `info()` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]  # Extract only the version number
    return f'Fish Shell {version}'
```

By splitting the output by `', '` and selecting the second part (the version number), we can ensure that only the version number is included in the formatted output.

This fix should address the bug reported in the failing test and should align with the GitHub issue related to the recursive loop triggered by this function with Oh-My-Fish's TheFuck plugin.