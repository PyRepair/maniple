The bug in the `match` function is that it assumes that the script will always have at least two elements when split by spaces. However, the error message suggests that the first element is 'git' and the rest is the usage message. 

We should check if the script is 'git' and return True if it is. If not, we should return False.

Here is the corrected version:

```python
@git_support
def match(command):
    return command.script == 'git'
```

This corrected version will satisfy all the expected cases. 

For example, in the case where `command.script='git'`, the function will return True, which is expected. In the case where `command.script` is not 'git', the function will return False, which is also expected.