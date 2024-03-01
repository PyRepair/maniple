### Analysis:
- The class `Fish` contains a method `info` that is supposed to return the version and name of the current shell.
- The method uses `Popen` to execute a command to get the version of the shell.
- The failing test is asserting that the method should return `'Fish Shell 3.5.9'`.
- The error message indicates that the actual output is `'Fish Shell fish, version 3.5.9'`, highlighting a parsing issue or incorrect output format.


### Bug Location:
- The bug is likely due to how the shell version is being parsed from the output of the command executed using `Popen`.


### Cause of the Bug:
- The `info` method is reading the output using `proc.stdout.read()`, which reads the output as it is.
- The expected output `'Fish Shell 3.5.9'` is not matching the actual output `'Fish Shell fish, version 3.5.9'`, indicating a mismatch in parsing the version from the command output.


### Bug Fix Strategy:
- To fix the bug, we need to parse the version properly from the command output.
- The actual output can be parsed to extract the version number only, eliminating unnecessary text.


### Corrected Version:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        output = proc.stdout.read().decode('utf-8').strip()
        version = output.split(',')[1].strip()
        return f'Fish Shell {version}'
```

In the corrected version:
- The command is changed to `['fish', '--version']` to ensure the version information is retrieved correctly.
- The output is split by commas and the second part (version) is extracted and trimmed to get the exact version number.
- The formatted string includes the extracted version to return `'Fish Shell <version>'`.

This correction should resolve the issue and make the test pass successfully.