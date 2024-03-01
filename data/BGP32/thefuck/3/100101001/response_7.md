### Analysis
1. The function is supposed to retrieve the version of the Fish shell by executing a command in the Fish shell.
2. The function is currently fetching the version using the command 'echo $FISH_VERSION', but the test is expecting the version to be fetched using the command 'fish --version'.
3. The test is mocking the stdout read to return 'fish, version 3.5.9\n', but the function is not handling this format correctly.
4. The function is not executing the correct command to retrieve the Fish shell version.

### Bug Cause
The bug is caused by the function using the incorrect command to fetch the Fish shell version and not handling the format of the output correctly.

### Fix Strategy
1. Change the command used to fetch the Fish shell version to 'fish --version'.
2. Modify the function to handle the output format 'fish, version x.x.x\n' and extract the version number correctly.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    version = output.split(' ')[2]
    return f'Fish Shell {version}'
```