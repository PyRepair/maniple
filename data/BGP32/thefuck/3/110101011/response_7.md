### Analysis:
1. The `info` function in the `Fish` class is attempting to retrieve the version of Fish shell by executing a command using `Popen`.
2. The test function is mocking the stdout read value to simulate the output of the command.
3. The current implementation is using `echo $FISH_VERSION` as the command, which is incorrect based on the failing test assertion.
4. The failing test is checking for the version output by `fish --version`, while the function is using `echo $FISH_VERSION`.
5. This mismatch in the command being executed is causing the function to return the wrong version, leading to test failure.

### Fix Strategy:
1. Modify the command executed by `Popen` in the `info` function to be `fish --version` instead of `echo $FISH_VERSION`.
2. Update the function logic to read the correct version output based on the modified command.
3. Ensure that the function properly formats the version information before returning it.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(", ")[1].strip()
    return u'Fish Shell {}'.format(version)
``` 

By making these changes, the `info` function will execute the correct command to fetch the Fish shell version and format it appropriately for the output. This correction should address the failing test and resolve the issue reported on GitHub.