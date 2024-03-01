### Explanation
The buggy function is attempting to retrieve the Fish shell version by executing the command `echo $FISH_VERSION` and extracting the version number from the output. However, the test is specifically looking for the command `fish --version` and the output `'Fish Shell 3.5.9'`.

The error occurs because the test is providing a different command output format than what the function expects. This mismatch leads to the AssertionError as shown in the error message.

### Strategy for fixing the bug
To fix the bug, we need to modify the `info` function in the `Fish` class to execute the correct command and extract the version number in the expected format.

### Corrected version of the function
```python
class Fish(Generic):
    def info(self):
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(', version ')[1].strip()
        return f'Fish Shell {version}'
```

With this corrected version, the `info` function will execute the correct `fish --version` command, extract the version number in the expected format, and return 'Fish Shell 3.5.9' as required by the test.