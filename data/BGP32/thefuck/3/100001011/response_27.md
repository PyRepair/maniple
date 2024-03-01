### Bug Explanation
The bug in the `info` function of the `fish.py` file is triggered by the way it reads the output of the `fish -c 'echo $FISH_VERSION'` command. The issue arises because the `proc.stdout.read()` method is being called before the process has finished executing. This causes the function to hang or produce incorrect output, leading to the reported problem in the GitHub issue.

### Bug Fix Strategy
To fix the bug, we need to ensure that the process completes before reading its output. One way to achieve this is by waiting for the process to finish using the `communicate()` method of the `proc` object. This will prevent the function from hanging and provide the correct version information.

### Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    out, _ = proc.communicate()
    version = out.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In the corrected version, we use `proc.communicate()` to wait for the process to finish and retrieve the output. Then, we decode the output to a string and strip any extra characters before returning the version information. This fix should prevent the function from hanging and resolve the issue reported on GitHub.