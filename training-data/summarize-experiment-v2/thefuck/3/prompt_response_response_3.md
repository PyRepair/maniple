The problem with the current implementation of the `info` function in the `Fish` class is that it is fetching the version of Fish shell using the command `fish -c 'echo $FISH_VERSION'`, but the actual command being used in the failing test is `fish --version`. This inconsistency between the actual command and the command being tested is causing the test to fail.

To fix this issue, the `info` function should be updated to use the correct command to fetch the version of Fish shell.

Here's the corrected code for the `info` function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '--version'], stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

With this correction, the function will use the correct command to fetch the version of Fish shell, and it should pass the failing test. Additionally, it will also resolve the issue posted in the GitHub repository related to Oh-My-Fish's TheFuck plugin triggering a recursive loop.

The updated GitHub issue title and description would be:

#### GitHub issue title:
`TheFuck plugin triggers recursive loop in Oh-My-Fish with Fish Shell`

#### GitHub issue description:
`Oh-My-Fish's TheFuck plugin triggers a recursive loop in Fish shell due to inconsistency in version fetching command. Fixed by updating the command in the `Fish.info()` function.`