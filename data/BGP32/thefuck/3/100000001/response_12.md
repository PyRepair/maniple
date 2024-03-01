The bug in the provided function lies in the way it reads the output from the subprocess. The `proc.stdout.read()` method reads the entire output stream from the subprocess, which may lead to a blocking issue depending on the subprocess execution.

To fix this bug, it is recommended to use `communicate()` method of the subprocess.Popen object, which reads the output in a non-blocking manner. By using this method, we can safely retrieve the output and avoid potential blocking issues.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    stdout, _ = proc.communicate()
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
```

In this corrected version, we use the `communicate()` method to read the output from the subprocess, ensuring that it is done in a non-blocking manner. This should prevent any potential blocking issues that may arise when reading subprocess output.