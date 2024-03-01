### Analysis:
1. The function `info` in the `fish.py` file of the `thefuck` project is supposed to return the name and version of the current shell (Fish Shell).
2. The function uses a `Popen` subprocess to execute `fish -c 'echo $FISH_VERSION'` command and fetch the output to get the version of the Fish Shell.
3. The bug occurs when the `info` function is called recursively due to the usage of the `thefuck -v` command by the Oh-My-Fish plugin. This recursive calling leads to a hang in the initialization of the Fish Shell.
4. To fix this bug, we need to prevent the recursive calling of the `info` function when `thefuck -v` command is executed.

### Bug Fix Strategy:
1. Check if the current execution is due to the `thefuck -v` command and skip the version retrieval in such cases to avoid the recursive calling.
2. Add a condition to handle the specific case of `thefuck -v` command and return a message acknowledging that the version retrieval is skipped.

### Corrected Version:

```python
def info(self):
    """Returns the name and version of the current shell"""
    if self._is_thefuck_v():
        return u'Fish Shell (version retrieval skipped due to thefuck -v command)'
    
    proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                 stdout=PIPE, stderr=DEVNULL)
    version = proc.stdout.read().decode('utf-8').strip()
    return u'Fish Shell {}'.format(version)
    
def _is_thefuck_v(self):
    # Check if called due to 'thefuck -v' command
    return len(sys.argv) > 1 and sys.argv[1] == '-v'
```

In the corrected version:
- The `info` function now checks if it is called due to the `thefuck -v` command using the `_is_thefuck_v` helper function. If so, it returns a message that the version retrieval is skipped.
- If not called due to `thefuck -v`, it proceeds with fetching the version of the Fish Shell and returning it.