# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
@git_support
def match(command):
    return (command.script.split()[1] == 'stash'
            and 'usage:' in command.stderr)

```

The github issue message is:
# A GitHub issue title for this bug
```text
git_fix_stash rule fails when script is just git
```

## The associated detailed issue description
```text
thefuck master 🔧  git
usage: git [--version] [--help] [-C <path>] [-c name=value]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p|--paginate|--no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]

The most commonly used git commands are:
   add        Add file contents to the index
   bisect     Find by binary search the change that introduced a bug
   branch     List, create, or delete branches
   checkout   Checkout a branch or paths to the working tree
   clone      Clone a repository into a new directory
   commit     Record changes to the repository
   diff       Show changes between commits, commit and working tree, etc
   fetch      Download objects and refs from another repository
   grep       Print lines matching a pattern
   init       Create an empty Git repository or reinitialize an existing one
   log        Show commit logs
   merge      Join two or more development histories together
   mv         Move or rename a file, a directory, or a symlink
   pull       Fetch from and integrate with another repository or a local branch
   push       Update remote refs along with associated objects
   rebase     Forward-port local commits to the updated upstream head
   reset      Reset current HEAD to the specified state
   rm         Remove files from the working tree and from the index
   show       Show various types of objects
   status     Show the working tree status
   tag        Create, list, delete or verify a tag object signed with GPG

'git help -a' and 'git help -g' lists available subcommands and some
concept guides. See 'git help <command>' or 'git help <concept>'
to read about a specific subcommand or concept.
thefuck master 🗡  fuck
[WARN] Rule git_fix_stash:
Traceback (most recent call last):
  File "/usr/local/lib/python3.4/dist-packages/thefuck/types.py", line 211, in is_match
    if compatibility_call(self.match, command):
  File "/usr/local/lib/python3.4/dist-packages/thefuck/utils.py", line 224, in compatibility_call
    return fn(*args)
  File "<string>", line 2, in match
  File "/usr/local/lib/python3.4/dist-packages/thefuck/specific/git.py", line 32, in git_support
    return fn(command)
  File "/usr/local/lib/python3.4/dist-packages/thefuck/rules/git_fix_stash.py", line 8, in match
    return (command.script.split()[1] == 'stash'
IndexError: list index out of range
----------------------------
```



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No."


