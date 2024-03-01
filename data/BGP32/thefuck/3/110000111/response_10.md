## Analysis:
1. The `info` function is meant to return the name and version of the current shell, Fish Shell in this case.
2. The function uses `Popen` to run a command (`echo $FISH_VERSION`) in the Fish shell and capture the output to get the version.
3. The bug occurs due to trying to read from `proc.stdout` without waiting for the process to complete.
4. The bug creates a recursive loop when the `info` function is called within the context mentioned in the GitHub issue.
   
## Strategy for Fixing the Bug:
1. Ensure that the `Popen` process completes before trying to read from `proc.stdout`.
2. Use `proc.communicate()` to wait for the process to finish and obtain both the output and error streams.
   
## Code Fix:
```python
class Fish(Generic):
    
    def info(self):
        """Returns the name and version of the current shell"""
        proc = Popen(['fish', '-c', 'echo $FISH_VERSION'],
                     stdout=PIPE, stderr=DEVNULL)
        out, _ = proc.communicate()
        version = out.decode('utf-8').strip()
        return u'Fish Shell {}'.format(version)
``` 

By using `proc.communicate()`, we ensure that the process completes before reading the output, avoiding the recursive loop issue.