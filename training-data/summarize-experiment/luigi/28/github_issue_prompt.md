You have been provided with a GitHub issue that details a bug. Your task is to create a summary of it, aiming for a comprehensive and insightful output. This thorough analysis is intended to enhance the efficiency and effectiveness of the debugging process.

# A GitHub issue title for this bug
```text
hive table_exists should be case insensitive?
```

## The associated detailed issue description
```text
Any thoughts on this one?\n\nIn https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L141\n(possibly here too, but we're not on CDH: https://github.com/spotify/luigi/blob/master/luigi/contrib/hive.py#L192)\n\nSometimes we have tables that are defined as capitalized, rather than lower case underscored names. These are easier to read in code if left capitalized, though hive is case insensitive, and will return them as lower case.\n\nE.g. when checking for an existing table table = 'FooBar', stdout will return with foobar and the test will fail\n\nThis wasn't an issue in older versions, which just checked for string \"does not exist\" or \"Table not found\" in stdout.\n\nWould be easy to fix using return stdout and table.lower() in stdout or return stdout and table.lower() in stdout.lower()\n\nLet me know your thoughts on this. I can supply a pull request if necessary.\n\nThanks,\nLin.
```

# A GitHub issue title for this bug
```text
Fix #896: make table_exists case insensitive
```

## The associated detailed issue description
```text
Check stdout against table.lower() to avoid case issues
```

