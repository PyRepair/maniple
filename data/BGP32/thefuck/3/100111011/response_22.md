### Bug Analysis:
1. The `info` function is intended to return the name and version of the current shell by executing a command. However, the command executed in the `Popen` call is incorrect. It is using `'fish -c echo $FISH_VERSION'` instead of `'fish --version'` which is causing the version extraction error.
2. The failing test `test_info` asserts that the expected output should be `'Fish Shell 3.5.9'`, but due to the incorrect command, the output ends up being `'Fish Shell fish, version 3.5.9'`.
3. The error indicates the mismatch between the expected output and the actual output. The runtime values of variables at the function's return also indicate the incorrect version extraction process.
4. To fix the bug, the command in the `Popen` call should be changed to `'fish --version'` to retrieve the correct version information.

### Corrected Version:
```python
# The corrected version of the buggy function
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version.split(',')[1].strip())

```

Correcting the command in the `Popen` call to `'fish --version'` ensures that the correct version information is extracted and returned without any extraneous characters. This fix should address the bug reported in the failing test and the GitHub issue.