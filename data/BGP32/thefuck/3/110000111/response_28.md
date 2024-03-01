To fix the bug in the `info` function within the `Fish` class, we need to ensure that the `Popen` object is used correctly and that the process is properly handled for reading the output. The current issue seems to be related to the way the subprocess is handled, causing hangs and recursive loops as described in the GitHub issue.

Here is a corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

In this corrected version:
- The `proc.communicate()` method is used to read the output from the process while also closing the pipes to prevent hangs.
- The `version` variable is populated correctly by decoding the output from the process.
- The function now properly handles the subprocess communication, avoiding the recursive loop issue described in the GitHub bug report.

This corrected version should now properly retrieve the version of the Fish Shell without causing any hangs or recursive loops.