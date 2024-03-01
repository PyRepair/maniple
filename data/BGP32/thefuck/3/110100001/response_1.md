## Analysis:
1. The buggy function `info` in the class `Fish` is using `Popen` to run a command `echo $FISH_VERSION` to get the version of the Fish shell.
2. The test case provided expects the version output to be `fish, version 3.5.9\n`, but the buggy function is not handling this format correctly.

## Bug Cause:
The bug is caused by the fact that the command run in the `Popen` call in the `info` function is `'echo $FISH_VERSION'`, but the test case expects `'fish, version 3.5.9\n'`, which is different.

## Strategy for Fixing the Bug:
1. Adjust the command passed to `Popen` in the `info` function to match the expected output in the test case.
2. Modify the decoding of the output to match the expected version format.

## Corrected Version of the Buggy Function:
```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(',')[1].strip()
        return f'Fish Shell {version}'
```

By updating the `Popen` command to `['fish', '--version']`, reading the output correctly, and parsing the version from the output, the corrected function should now pass the failing test.