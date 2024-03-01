## Analysis:
1. The `info` function within the `Fish` class is trying to retrieve the version of the Fish shell by executing a command through `Popen`.
2. The `Popen` function is used to run a command in a sub-process.
3. The issue lies in reading the output from the process using `proc.stdout.read().decode('utf-8')`, as it may not return the output immediately and may block indefinitely.
4. To fix this, we can use `communicate()` method of `Popen` to read the output and avoid blocking issues.

## Bug Fix:
```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        out, _ = proc.communicate()
        version = out.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

By using `proc.communicate()`, we ensure that the output is read and decoded properly without blocking the process. This will prevent the bug from occurring and provide the correct version of the Fish shell.