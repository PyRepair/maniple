## Analysis
1. The `info` function in the `fish.py` shell module aims to retrieve the version of the Fish shell by running `echo $FISH_VERSION` command. However, the expected version does not match the actual version due to incorrect processing.
   
2. The `Popen` call is using `['fish', '-c', 'echo $FISH_VERSION']`. This command will return the entire string `'fish, version 3.5.9'` instead of just the version number.

3. The failing test checks if the returned value from `shell.info()` is `"Fish Shell 3.5.9"`, but it actually gets `"Fish Shell fish, version 3.5.9"`.

4. To fix the bug, we need to extract just the version number from the output obtained and include it in the return message.

## Bug Fix
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip().split(', ')[1].split()[1]
    return u'Fish Shell {}'.format(version)
```

With this fix, we extract the version number correctly and include it in the return message. The corrected function should now return the expected value and pass the failing test.