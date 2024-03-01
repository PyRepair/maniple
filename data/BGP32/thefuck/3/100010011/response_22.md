### Analysis:
1. The `info` function in the `fish.py` file of the `thefuck` package is attempting to retrieve the version of the Fish shell by running the command `fish -c 'echo $FISH_VERSION'`. 
2. The failing test in the `test_info` method is mocking the output of the `Popen` call to return `b'fish, version 3.5.9\n'`, however, the function is expecting just the version number without the additional text.
3. The root cause of the bug is that the `info` function is not correctly handling the output of the `Popen` call, resulting in the additional text "fish, version" being included in the version string.
4. To fix the bug, we need to modify the `info` function to properly extract and format the version number from the output of the `Popen` call.

### Fix Strategy:
1. Instead of reading the whole output from the `Popen` call, we need to parse out just the version number.
2. We should split the output string by comma and whitespace to extract the version number.
3. We then format the extracted version number into the desired format before returning it.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(',')[1].strip()
    return u'Fish Shell {}'.format(version)
```

By making these changes to the `info` function, the corrected version should properly extract the version number from the output of the `Popen` call and return it in the expected format.