## Analysis
The problem in the `info` function lies in the command being executed to get the Fish shell version. The actual command should be `'fish', '--version'` instead of `'fish', '-c', 'echo $FISH_VERSION'`. Additionally, the assertion in the test is checking for the expected output using the incorrect output format from the current implementation.

## Bug Explanation
- The current implementation of the `info` function does not fetch the version correctly using `echo $FISH_VERSION`, which leads to the incorrect version being returned.
- The test is expecting the version to be in the format `'Fish Shell 3.5.9'` but due to the incorrect output of the command, the wrong format is returned which leads to the assertion error.

## Fix Strategy
The fix involves modifying the command to retrieve the Fish shell version correctly using `'fish', '--version'` and adjusting the test to match the expected output format.

## Corrected Version
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split(' ')[2].rstrip('\n'))
```

With this correction, the function will correctly fetch the Fish shell version and format it in the expected way. It will then pass the failing test, thus resolving the issue reported on GitHub.