To fix the bug in the provided function `info`, we need to address the issue where the function hangs when attempting to retrieve the Fish Shell version. The problem lies in how the `Popen` process is handled, specifically reading its output. The correct approach is to wait for the process to finish before reading the output.

Here are the steps to fix the bug in the `info` function:
1. Use the `communicate()` method of the `Popen` object to wait for the process to finish and retrieve its output.
2. Decode the output to UTF-8 after calling `communicate()`.
3. Trim any leading or trailing whitespace from the decoded version string.

Below is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()`, we ensure that the process completes before reading its output. This approach should prevent the hang issue experienced when trying to fetch the Fish Shell version.