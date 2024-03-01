The bug in the `info` function of the `Fish` class is related to a recursive loop triggered by the `thefuck -v` command used in the Oh-My-Fish plugin. This recursive loop occurs due to the command `thefuck -v` calling the `Fish.info()` function, causing infinite recursion.

To fix this bug, we need to prevent the `info` function from being called when the command `thefuck -v` is used. One way to achieve this is by checking the command that is being executed and returning an empty string if it matches `thefuck -v`.

Here is the corrected version of the `info` function:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        if 'thefuck -v' in ' '.join(sys.argv):
            return ''  # Prevent infinite recursion
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By checking if the command contains `'thefuck -v'` before proceeding with the shell version retrieval, we ensure that the infinite recursion issue triggered by the `thefuck -v` command is avoided.

This fix addresses the GitHub issue by preventing the recursive loop in the `Fish.info()` function when the command `thefuck -v` is used.