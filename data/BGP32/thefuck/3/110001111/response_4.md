To fix the bug in the `info` function of the `Fish` class in `fish.py`, we need to address the issue where the function `info` is returning the entire version string including the prefix "fish, version". The expected output should only contain the version number.

Here's the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        # Extract only the version number from the version string
        version_number = version.split(", version ")[1]
        return u'Fish Shell {}'.format(version_number)
```

By splitting the version string and extracting only the version number, we ensure that the output of the `info` function is as expected.

This correction will resolve the issue reported on GitHub regarding the recursive loop caused by the incorrect version string returned by the `info` function when using the `-v` option with TheFuck plugin in Oh-My-Fish.