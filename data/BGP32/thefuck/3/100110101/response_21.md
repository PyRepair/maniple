## Analysis
The buggy function `info` is supposed to retrieve the version of the Fish shell by executing a command and reading the output. However, there are multiple issues in the implementation:
1. The command used to retrieve the version (`echo $FISH_VERSION`) does not match the one used to set the version in the test (`fish, version 3.5.9\n`).
2. The assertion in the test does not match the expected output due to the mismatch in the command output.
3. The function is stripping the version but not filtering out everything else, causing the mismatch in output.

## Solution
To fix the bug, the function should properly execute the command to retrieve the version of Fish shell and then format the output according to the expected output in the test.

## The corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.replace('fish, version ', '')
    return 'Fish Shell {}'.format(version)
``` 

By updating the command to `['fish', '--version']`, reading and stripping the output correctly, and then extracting the version from the output, the function now behaves as expected.