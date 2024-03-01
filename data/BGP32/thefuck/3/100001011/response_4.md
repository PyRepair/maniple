There are a few potential issues causing the bug in the 'info' function:
1. The function is trying to read from proc.stdout multiple times, which could result in an incorrect or empty value.
2. The decoding of the output using 'utf-8' might not be successful in certain cases.
3. The way the version is extracted from the command output may not be accurate.

To fix the bug, we should wait for the process to finish before reading from proc.stdout, use proper error handling for decoding the output, and ensure that the version is extracted correctly.

Here is the corrected version of the 'info' function:

```python
def info(self):
    """Returns the name and version of the current shell"""
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'], stdout=PIPE, stderr=DEVNULL)
    out, _ = proc.communicate()
    
    try:
        version = out.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
    except UnicodeDecodeError:
        return None
```

This version uses the communicate() method to read the output after the process finishes, adding error handling for decoding the output. 