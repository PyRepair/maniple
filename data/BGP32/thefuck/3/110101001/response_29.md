### Analysis
The bug in the `info` function is caused by using the incorrect command to retrieve the Fish shell version. The command `echo $FISH_VERSION` is being used instead of `fish --version`, leading to incorrect output. Additionally, the test expects the version number to be in the format `Fish Shell 3.5.9`, but the actual output includes extra characters such as `, version`.

### Strategy for fixing the bug
1. Update the command in the `Popen` call to `'fish', '--version'` to retrieve the correct Fish shell version.
2. Modify the output formatting to match the expected output format `Fish Shell {version}`.

### Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip().split(',')[1].strip()
        return u'Fish Shell {}'.format(version)
```