### Identified issues:
1. The command being executed in the `Popen` function is `'fish', '-c', 'echo $FISH_VERSION'` instead of `['fish', '--version']`.
2. The expected output in the test is `'fish, version 3.5.9\n'`, whereas the function is expecting only `'3.5.9'` without the additional text.

### Bug cause:
The bug is caused by the incorrect command being executed in the `Popen` function. Additionally, the function is not handling the extra text in the version output correctly.

### Strategy for fixing the bug:
1. Update the command in the `Popen` function to `['fish', '--version']` to correctly fetch the version information.
2. Modify the function to extract only the version number from the output and format it along with the shell name.

### Corrected version of the function:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'],
                 stdout=PIPE, stderr=DEVNULL)
    # Extracting the version number by splitting the output
    version = proc.stdout.read().decode('utf-8').strip().split()[-1]
    return u'Fish Shell {}'.format(version)
```

By making these changes, the function will correctly fetch the shell version information, extract only the version number, and format it along with the shell name. This corrected version should pass the failing test.