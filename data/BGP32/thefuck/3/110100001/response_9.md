### Analysis:
1. The `info` function in the `Fish` class is supposed to return the name and version of the current shell by executing a command in the fish shell.
2. The `info` function uses `Popen` to run the command `echo $FISH_VERSION` in the fish shell and capture the output to extract the version.
3. The failing test sets up a mock `Popen` object to return `b'fish, version 3.5.9\n'`, but the expected version string is 'Fish Shell 3.5.9'.
4. The bug is caused by the incorrect shell command used in `Popen` and the incorrect decoding of the output.

### Bug:
The bug is caused by using the incorrect command `echo $FISH_VERSION` instead of `fish --version` in the `Popen` call. Additionally, the decoding of the output is incorrect.

### Fix Strategy:
1. Update the command in the `Popen` call to `'fish', '--version'` to get the correct version information from the fish shell.
2. Update the decoding of the output to correctly extract the version string.
3. Modify the test to match the correct expected version string 'Fish Shell 3.5.9'.

### Corrected Version:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(' ')[2]
        return f'Fish Shell {version}'
```

### Test:
```python
def test_info(self, shell, Popen):
    Popen.return_value.stdout.read.side_effect = [b'fish, version 3.5.9\n']
    assert shell.info() == 'Fish Shell 3.5.9'
    assert Popen.call_args[0][0] == ['fish', '--version']
``` 

After applying the fix and running the test, the corrected version of the function should pass the failing test.