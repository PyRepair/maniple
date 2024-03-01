## Error Location
The error in the `info(self)` function lies in how it reads the output of the subprocess. The code reads the output of the subprocess using `proc.stdout.read().decode('utf-8').strip()`, which can cause issues if the subprocess output is not immediately available or is too large.

## Bug Cause
The buggy code reads the subprocess output directly without waiting for the process to finish or checking for errors. This can lead to issues like hanging when the subprocess output is not immediately available.

## Fix Strategy
To fix this bug, we need to wait for the subprocess to finish and handle any errors that may occur during the process. This can be achieved by using `proc.communicate()` instead of directly reading the output.

## Corrected Version
```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    
    stdout, _ = proc.communicate()
    if proc.returncode != 0:
        return "Fish Shell not found"
    
    version = stdout.decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

In the corrected version, we use `proc.communicate()` to wait for the subprocess to finish and get both the stdout and stderr. We then check if the return code is non-zero, indicating an error, and handle it accordingly. This approach ensures the subprocess output is properly retrieved and any errors are handled gracefully.