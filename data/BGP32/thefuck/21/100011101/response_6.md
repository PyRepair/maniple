The bug in the function is caused by trying to access the second element of the split command script without checking if it exists. This results in an IndexError when the script does not contain any spaces.

To fix this bug, we need to first check if the script has at least two parts after splitting before accessing the second part.

Here is the corrected version of the function:

```python
@git_support
def match(command):
    splited_script = command.script.split()
    return (len(splited_script) > 1 and splited_script[1] == 'stash'
            and 'usage:' in command.stderr)
```

With this correction, we ensure that the script is split and has at least two parts before trying to access the second part. This should prevent the IndexError and make the function work correctly.