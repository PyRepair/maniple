## Analysis:
1. The `info` function is supposed to return the name and version of the current shell (Fish shell) by executing a command in the Fish shell and capturing the version.
2. The function uses `Popen` to execute a command `fish -c 'echo $FISH_VERSION'` and capture the output to get the version number of Fish shell.
3. The failing test `test_info` sets up `Popen` to return `b'fish, version 3.5.9\n'` when the subprocess is executed.
4. The bug seems to be in the command used to extract the version from the output of the command. The command used in the function is not matching the output simulated in the test.

## Bug Fix Strategy:
To fix the bug, the command used in the `Popen` call needs to be updated to match the output produced in the test. Additionally, we need to correct the assertion in the test to match the correct command used in the function.

## Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[-1]  # Extracting the version number
        return 'Fish Shell {}'.format(version)
```

In the corrected version, the command executed in the `Popen` call has been updated to `['fish', '--version']` to match the output provided in the failing test. The version number is correctly extracted by splitting the output and taking the last element.