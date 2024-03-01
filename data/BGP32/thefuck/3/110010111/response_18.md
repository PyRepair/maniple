## Analysis
1. **Buggy Function and Class Relationship**: The `info` function is a method of the `Fish` class in the `fish.py` file under the `thefuck.shells` module. The function is supposed to return the name and version of the current shell.
   
2. **Error Message**: The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the version string obtained from the command is not being processed correctly.

3. **Expected Input/Output Values**:
   - Input: The output of the `echo $FISH_VERSION` command should be `'3.5.9'`.
   - Expected Output: `'Fish Shell 3.5.9'`.

4. **GitHub Issue**: The issue is related to a recursive loop triggered by the use of the `-v` flag with `thefuck` in Fish shell initialization with Oh-My-Fish plugin. The buggy function in `fish.py` contributes to this problem.

## Bug Cause
The bug is caused by not properly handling the output of the `echo $FISH_VERSION` command. The incorrect processing of the obtained version string results in the mismatch between the expected and actual output values.

## Fix Strategy
To fix the bug, we need to ensure that the version string extracted from the command output is processed correctly before formatting and returning it as the shell information.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return u'Fish Shell {}'.format(version)
```

By splitting the version string obtained from `proc.stdout.read()` by `', '`, we extract only the version number itself, resulting in the correct formatted output as `'Fish Shell 3.5.9'`. This change ensures proper handling of the version information retrieved from the command output.