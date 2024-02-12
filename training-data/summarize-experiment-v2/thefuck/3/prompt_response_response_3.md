There seems to be a problem with the `info` function in the `Fish` class. The function is supposed to return the name and version of the current shell, but it is currently just returning the version number. This is causing the failing test to not match the expected output, resulting in a failing test case.

To fix this, we need to modify the function to properly format and return both the name and the version number of the shell.

Here is the corrected function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '--version'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

With this fix, the function now properly runs `fish --version` command to get the complete version string and then formats it as "Fish Shell <version>", which matches the expected output. This corrected function should pass the failing test and resolve the issue posted in GitHub.

This fix resolves the problem by correctly formatting the output to include the name of the shell as well as the version number. This will ensure that the function returns the expected value and satisfies the failing test case.

Please replace the existing `info` function in the `Fish` class with the corrected code provided above to resolve the issue.