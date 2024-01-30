# Prompt Github issue info based facts

Your task is to determine whether the provided fact would be useful and relevant to fixing the buggy function.
Assume you know the buggy function source code,
does following github issue message helps to fix the bug?

The buggy function's source code is:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False

```

The github issue message is:
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



Your response should follow this format:
Justification: <your justification>
Conclusion: either "Yes." or "No." 

Please be selective in your evaluation. Longer prompts with numerous insignificant facts could diminish the effectiveness of a large language model (LLM) in generating a successful patch for the bug. Only facts that are deemed significantly contributory (Conclusion: "Yes.") will be utilized as input for the LLM to facilitate the repair of the buggy function.


