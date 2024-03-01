### Bug explanation
The bug in the `info` function lies in the way the version information is extracted from the output of the subprocess. The current implementation retrieves the version information along with the shell name which results in incorrect output. This is evident from the input and output values observed during test execution.

### Bug fix strategy
To fix the bug, we need to modify the command executed by the subprocess to only retrieve the version number without any additional text. This can be achieved by modifying the command passed to the `Popen` constructor.

### Corrected version of the function
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION | awk -F, \'{print $2}\''],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

By adding the `awk -F, '{print $2}'` command to the subprocess, we extract only the version number from the output, resolving the bug and providing the expected output.