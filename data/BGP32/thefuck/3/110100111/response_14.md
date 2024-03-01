## Analysis:
1. The `info` function in the `Fish` class is trying to get the version of Fish shell by running the command `fish -c 'echo $FISH_VERSION'` using `Popen`. However, the expected version is not being captured correctly.
2. The failing test sets the side effect for `Popen.return_value.stdout.read` to return `b'fish, version 3.5.9\n'`, but the function is not handling this input correctly.
3. The `info` function is expecting the version number in the format `x.y.z` but the output from `Popen` is not parsed correctly causing the function to fail.
4. To fix the bug, we need to update the function to correctly handle the output from `Popen` and extract the correct version number.

## Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        version = proc.stdout.read().decode('utf-8').strip()
        version = version.split(', version ')[1].split('\n')[0]  # Extract the version number
        return u'Fish Shell {}'.format(version)
```

After making the above fix, the `info` function should now correctly parse the version number from the output of `Popen` and return it in the expected format.

This fix should resolve the issue posted on GitHub related to the recursive loop caused by using the `thefuck -v` command in Fish shell with Oh-My-Fish plugin.