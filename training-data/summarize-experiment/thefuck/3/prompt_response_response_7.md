The error is occurring in the `info` function of the `Fish` class. The function is supposed to return the name and version of the current shell, but it's currently not correctly parsing the version information and is returning just the version number without the shell name.

The reason for the bug is that the command `echo $FISH_VERSION` is being used to get the version, but the output of this command includes the shell name ("fish") along with the version number. The current implementation is only extracting the version number and not including the shell name.

To fix the bug, we need to modify the command to retrieve the version information in a way that includes both the shell name and the version number. Then, we need to update the parsing logic in the function to correctly extract both the shell name and the version number.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version_output = proc.stdout.read().decode('utf-8').strip()
    shell_name, version = version_output.split(', version ')
    return u'{} {}'.format(shell_name, version)
```

This fixed version of the function retrieves the shell name and version number using the command `fish --version` and then correctly parses the output to extract both pieces of information. This should resolve the issue and ensure that the function returns the correct shell name and version.