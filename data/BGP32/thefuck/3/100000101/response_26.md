The bug in the provided function is that the `Popen` process is not being waited for, causing the `proc.stdout.read()` to potentially return an empty value or inaccurate result. This is because the `Popen` process runs asynchronously without waiting for it to finish before reading the stdout.

To fix this bug, we should use the `communicate()` method of the `Popen` object, which will wait for the process to finish before reading the output. 

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

By using `proc.communicate()`, we ensure that the process is completed before reading the output, thus providing the accurate version value.