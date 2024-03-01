### Analysis:
The error message indicates that the expected output is `'Fish Shell 3.5.9'`, but the actual output is `'Fish Shell fish, version 3.5.9'`. This suggests that the `info` function is not correctly extracting the version number from the output of the `fish -c 'echo $FISH_VERSION'` command.

Looking at the runtime values, we see that the `version` variable is being assigned the value `'fish, version 3.5.9'`, which is not just the version number. This indicates that the issue lies in how the version number is extracted from the output of the `Popen` command.

### Bug:
The bug is caused by the incorrect extraction of the version number from the `Popen` command output. The string `'fish, version 3.5.9'` includes the shell name 'fish' and the version number '3.5.9' separated by a comma, and the function is not correctly parsing this output.

### Fix:
To fix the bug, we need to modify the way we extract the version number from the command output. We can split the output string by the comma and take the second part as the version number.

### Corrected version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    output = proc.stdout.read().decode('utf-8').strip()
    shell_name, version = output.split(', version ')
    return u'Fish Shell {}'.format(version)
``` 

This corrected version splits the output string by the comma and then further splits the resulting parts by the string `', version '`, assigning the second part to the `version` variable. This ensures that only the version number is extracted and returned as the shell information.