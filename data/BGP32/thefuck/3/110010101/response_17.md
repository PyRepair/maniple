### Analysis
1. The `info` function in the `Fish` class is supposed to retrieve the version of the Fish shell and return it in a specific format. However, the current implementation is not correctly extracting the version string from the output.
2. The error message indicates that the extracted version contains extra information ("fish, version").
3. The cause of the bug is the incorrect formatting of the output string. The `echo $FISH_VERSION` command returns the version with extra information, leading to the unexpected output.
4. To fix the bug, we need to modify the command in the `Popen` call to only extract the version number without any additional text.
5. We should extract only the version number and format the output as expected.

### Correction
```python
class Fish(Generic):

    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        
        # Extract version number only
        version = version.split(',')[1].strip()
        
        return u'Fish Shell {}'.format(version)
```

This corrected version of the `info` function will correctly extract the version number from the output of the `echo $FISH_VERSION` command, leading to the expected output format.