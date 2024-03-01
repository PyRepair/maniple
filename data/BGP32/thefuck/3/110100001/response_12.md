## Analysis:
1. The `info` function in the `Fish` class is supposed to return the name and version of the Fish shell.
2. The function uses `Popen` to execute a command to get the version of the Fish shell.
3. The failing test shows that the expected version is `'Fish Shell 3.5.9'`, but the actual version retrieved from the command output is `b'fish, version 3.5.9\n'`.
4. The bug is likely caused by the incorrect command being executed to retrieve the version of the Fish shell.

## Bug Fix Strategy:
1. Update the command passed to `Popen` to retrieve the Fish shell version correctly.
2. Modify the test case to ensure that the correct command is being used and compare the output accordingly.

## Corrected Version:
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(', version ')[1].strip())

# Updated test function
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
```

By using the `--version` flag in the command passed to `Popen`, the correct version of the Fish shell will be retrieved. Additionally, updating the test case to check the correct command arguments ensures that the function is being called with the right parameters.