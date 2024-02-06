```python
from thefuck.utils import replace_argument
from thefuck.specific.git import git_support

@git_support
def get_new_command(command):
    try:
        upstream_option_index = command.script_parts.index('--set-upstream')
    except ValueError:
        upstream_option_index = -1

    try:
        if upstream_option_index == -1:
            upstream_option_index = command.script_parts.index('-u')
    except ValueError:
        pass
    
    if upstream_option_index != -1:
        command.script_parts.pop(upstream_option_index)
        command.script_parts.pop(upstream_option_index)

    push_upstream = command.stderr.split('\n')[-3].strip().partition('git ')[2]
    return replace_argument(" ".join(command.script_parts), 'push', push_upstream)
```