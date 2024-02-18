The issue appears to be related to the `Fish.info` function in the `shells/fish.py` file. It seems to hang during initialization when the `thefuck` plugin tries to use `thefuck -v` to regenerate functions. The specific issue is triggered by a recursive loop due to the `shells/fish.py:Fish.info()` function.

The error message is not mentioned, but I can see from the GitHub issue that it is causing a recursive loop during initialization of the Oh-My-Fish plugin due to an issue with the `Fish.info` function.

To fix the issue, the specific problem in the `Fish.info` function needs to be addressed to prevent the recursive loop.

The `Fish.info` function is attempting to retrieve the version of the Fish shell using the command `echo $FISH_VERSION`. The problem may be related to how the function hangs when trying to get the version.

To fix the problem, it might be necessary to change the way the version is retrieved or handle the recursive loop issue during initialization.

Here's a potential fix for the `Fish.info` function:

```python
def info(self):
    proc = Popen(['fish', '-c', 'set | grep FISH_VERSION | cut -d= -f2'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

This fix modifies the command to retrieve the Fish shell version and eliminates the recursive loop during initialization that is causing the hang. This change should resolve the issue reported on GitHub.