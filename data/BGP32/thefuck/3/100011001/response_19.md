### Bugs Identified:
1. The function is expecting the output of the command `echo $FISH_VERSION` to be a single line with only the version number, but the actual output includes extra text `fish, version`.
2. The function is not handling the case where the `stdout` is empty or does not contain the expected version number.

### Bug Fix Strategy:
1. Modify the function to extract only the version number from the output of the command.
2. Handle the case where the `stdout` is empty or does not contain the version number appropriately.

### Corrected Version:
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    version = version_output.split(", version ")[1] if ", version " in version_output else version_output
    return u'Fish Shell {}'.format(version.strip())
```