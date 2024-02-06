You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
Indentation is incorrectly changed for tabulated comments after a dedent
```

## The associated detailed issue description
```text
Operating system: Ubuntu 18.04
Python version: 3.6.3
Black version: master

Thank you @ambv for this library. When trying to run this on a codebase that uses tabs, indentation for comments past depth 0 is changed incorrectly after a dedent. Sample input (NB tabs):

if 1:
	if 2:
		pass
	# This comment should be indented the same as the next line
	pass
Black reformats this to:

if 1:
    if 2:
        pass
        # This comment should be indented the same as the next line
    pass
Note that this only happens when the input file uses tabs.
```

