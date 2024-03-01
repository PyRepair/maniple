The bug in the provided function is caused by directly reading from `proc.stdout` before waiting for the process to finish executing. This can result in an empty or incomplete output being read.

To fix this bug, we need to wait for the process to finish executing before reading from `proc.stdout`. We can achieve this by adding `proc.wait()` before reading from `proc.stdout`.

Here is the corrected version of the function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    proc.wait()  # Wait for the process to finish executing
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
``` 

By adding `proc.wait()` before reading from `proc.stdout`, we ensure that the process has completed and the output is available to be read. This correction should fix the bug and provide the expected output for the given test cases.