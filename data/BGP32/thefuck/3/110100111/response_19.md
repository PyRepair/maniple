## Bug Analysis:
1. The `info` function of the `Fish` class is supposed to retrieve the version of the Fish shell by executing `echo $FISH_VERSION` command.
2. The bug in the function is related to reading the output of the command execution and formatting it.
3. The failing test `test_info` sets the expected output as `'Fish Shell 3.5.9'`, but the actual output is not matching that due to the incorrect processing of the command output.
4. The GitHub issue mentions that the bug causes a loop due to the use of `-v` option, which implies that the issue could be related to how the version is fetched.

## Bug Fix Strategy:
1. Update the command used by `Popen` to get the Fish shell version.
2. Correctly read and format the output to fetch the version number.
3. Ensure the output matches the expected format.

## Corrected Version of the Bug Function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split()[2]  # Extract version from the output
        return f'Fish Shell {version}'
```

By updating the command to `['fish', '--version']`, correctly parsing the output to get the version number, and adjusting the return format, this corrected function should resolve the bug and pass the failing test.