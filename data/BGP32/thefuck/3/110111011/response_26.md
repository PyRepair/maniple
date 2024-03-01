### Bug Explanation

The bug in the `info` function of the `Fish` class is caused by the mismatch in the expected version output and the actual version output obtained from the `Popen` subprocess call. The failing test expects the version string to be `'Fish Shell 3.5.9'`, but due to the incorrect command `echo $FISH_VERSION` and the way the version output is read, it returns `'fish, version 3.5.9'`.

### Bug Fix Strategy

To fix the bug, the command executed by `Popen` needs to be modified to retrieve the version string correctly. Additionally, the way the output is read from the subprocess needs to be adjusted to match the expected format.

### Corrected Version

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version_bytes = proc.stdout.read().strip()
        version_str = version_bytes.decode('utf-8')
        version = version_str.split(',')[1].strip()
        return 'Fish Shell {}'.format(version)
```

With this correction, the `info` function will execute the correct command to obtain the Fish shell version and extract the version string correctly.