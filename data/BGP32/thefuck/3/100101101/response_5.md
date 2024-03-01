### Explanation:
The bug in the `info` function is caused by the incorrect command executed to fetch the Fish shell version. The command `['fish', '-c', 'echo $FISH_VERSION']` does not properly retrieve the version. Additionally, the `test_info` test case specifies the expected output as `'Fish Shell 3.5.9'`, but the actual version extracted from the command includes additional unnecessary characters and words ('fish, version').

### Strategy for Fixing the Bug:
1. Modify the command executed by `Popen` to retrieve the Fish shell version correctly.
2. Parse the obtained version to extract only the version number without any additional text.

### Corrected Version of the Function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version_with_text = proc.stdout.read().decode('utf-8').strip()
    version = version_with_text.split(', version ')[1]
    return f'Fish Shell {version}'
``` 

By using `['fish', '--version']` instead of `['fish', '-c', 'echo $FISH_VERSION']`, we correctly obtain the Fish shell version, and then extract only the version number from the string. This updated version of the function should now pass the failing test case.