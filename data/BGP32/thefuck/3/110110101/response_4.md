## Analysis
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell by executing a command and then return a formatted string including the version.
2. The error in the function seems to be related to the command executed and the processing of its output.
3. The failing test is setting up a mock `Popen` object to mimic the output of the command execution, but the comparison is failing due to incorrect formatting of the output.
4. To fix the bug, we need to modify the command executed to get the Fish shell version and adjust how we process the output of the command.

## Bug Fix Strategy
1. Update the command executed by `Popen` to get the Fish shell version correctly (replace `echo $FISH_VERSION` with `fish --version`).
2. Adjust the function to correctly process the output of the command to extract the version.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.readline().strip().decode('utf-8').split(', version ')[1]
        return 'Fish Shell {}'.format(version)
```