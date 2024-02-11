Shorter version of runtime input and output value pair:

## Case 1
### Runtime input
command.script_parts: ['git', 'push']
command.stderr: 'fatal: The current branch master has no upstream branch.'

### Runtime output
upstream_option_index: -1
push_upstream: 'push --set-upstream origin master'

## Case 2
### Runtime input
command.script_parts: ['git', 'push', '-u']
command.stderr: 'fatal: The current branch master has no upstream branch.'

### Runtime output
upstream_option_index: 2
push_upstream: 'push --set-upstream origin master'

## Case 3
### Runtime input
command.script_parts: ['git', 'push', '-u', 'origin']
command.stderr: 'fatal: The current branch master has no upstream branch.'

### Runtime output
upstream_option_index: 2
push_upstream: 'push --set-upstream origin master'

## Case 4
### Runtime input
command.script_parts: ['git', 'push', '--set-upstream', 'origin']
command.stderr: 'fatal: The current branch master has no upstream branch.'

### Runtime output
upstream_option_index: 2
push_upstream: 'push --set-upstream origin master'

## Case 5
### Runtime input
command.script_parts: ['git', 'push', '--quiet']
command.stderr: 'fatal: The current branch master has no upstream branch.'

### Runtime output
upstream_option_index: -1
push_upstream: 'push --set-upstream origin master'