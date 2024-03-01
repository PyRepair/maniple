Based on the information provided, the bug in the `info` function of the `Fish` class is due to the fact that the command to get the Fish version is incorrect, causing the test to fail.

Here's the corrected version of the `info` function:
```python
class Fish(Generic):
    def info(self):
        proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version.split()[-1])
```

Explanation of the bug and solution:
- The original code used `'echo $FISH_VERSION'` command to retrieve the Fish version, which wasn't correct. The test was expecting `['fish', '--version']` command instead.
- By fixing the command to `['fish', '--version']`, the correct Fish version can be obtained from the process output, which resolves the issue with the failing test.
- The corrected version splits the version string and extracts the actual version number from it to match the test's expected output.

This correction should resolve the failing test and address the GitHub issue related to the recursive loop caused by the incorrect command.