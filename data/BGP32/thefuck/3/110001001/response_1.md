Based on the provided information, the bug in the `info` function of the `Fish` class seems to be related to how the output of the `Popen` process is handled. The variable `version` is not correctly capturing the output value from the `Popen` process.

The issue likely arises because the `read` function is being called on `proc.stdout` before decoding it. 

To fix this bug, we need to ensure that the output is being read and then decoded before working with it.

Here is the corrected version of the `info` function:

```python
class Fish(Generic):
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
        stdout, _ = proc.communicate()
        version = stdout.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
```

In this corrected version, `proc.communicate()` is used to read the output of the `Popen` process and decode it before storing it in the `version` variable. This should fix the issue and correctly capture the version of the Fish shell.