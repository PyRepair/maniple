### Analysis:
1. The `info` function in the `Fish` class is supposed to retrieve the Fish shell version by running the command `fish -c 'echo $FISH_VERSION'`. However, the test is expecting the version to be '3.5.9' but the actual output includes additional text 'fish, version'.
2. The `assert Popen.call_args[0][0]` statement in the test is expecting `['fish', '--version']` but the actual command being executed is `['fish', '-c', 'echo $FISH_VERSION']`.

### Cause of the Bug:
The bug is caused by the incorrect command being executed to retrieve the Fish shell version. The output of the command includes additional text that should not be present which causes the test to fail.

### Strategy for Fixing the Bug:
1. Modify the command executed by `Popen` to `['fish', '--version']` to match the expected command in the test.
2. Update the parsing of the version to extract only the version number without any additional text.

### The corrected version of the function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(', ')[1]
        return u'Fish Shell {}'.format(version)
```

By updating the command to retrieve the version correctly and parsing the output to extract only the version number, the corrected function should now pass the failing test.