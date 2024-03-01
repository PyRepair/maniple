The bug in the `info` function of the `Fish` class is due to the incorrect command being used to get the Fish shell version. The command in the function is `'fish', '-c', 'echo $FISH_VERSION'`, but the expected command should be `'fish', '--version'`.

### Explanation of the bug

1. The provided test sets up the `Popen` mock object to return `b'fish, version 3.5.9\n'` when its `stdout.read` method is called.
2. The `info` function then creates a process using `'fish', '-c', 'echo $FISH_VERSION'` as the command to get the Fish version.
3. The process output is read and stripped to obtain the version `'fish, version 3.5.9'`.
4. Finally, the function constructs the return value as `'Fish Shell fish, version 3.5.9'`, leading to the assertion failure with the expected value `'Fish Shell 3.5.9'`.

### Strategy for fixing the bug

To fix this bug, we need to modify the command used to get the Fish shell version. We should change it from `'fish', '-c', 'echo $FISH_VERSION'` to `'fish', '--version'`.

### Corrected version of the function

```python
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(', version ')[1])
``` 

With this modification, the `info` function will correctly retrieve the Fish shell version using the `fish --version` command, and the test will pass successfully.