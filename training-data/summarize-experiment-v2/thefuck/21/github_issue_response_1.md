GitHub Bug Title:
Error when running 'git' commands

Description:
When running 'git' commands with only the word 'git' in the script, it results in an error. The error occurs when running the 'stash' command. This leads to a 'list index out of range' error in the 'git_fix_stash' rule.

Expected Output:
When running 'git' commands, including just the word 'git,' it should not result in an error, specifically when running the 'stash' command.

Environment:
- Python: 3.7.3.final.0
- numpy: 1.18.1
- matplotlib: 3.1.2
- scipy: 1.3.0
- xlrd: 1.2.0