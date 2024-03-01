## Bug Fix Strategy:
1. The bug arises from the case sensitivity issue in the comparison between the table name and the output from the Hive query. To resolve this, we need to ensure that the comparison is case insensitive.
2. Modify the comparison between the table name and the output to be case insensitive to address the bug.
3. Update the `table_exists` function to use case-insensitive comparison when checking if the table exists.

## Corrected Version of the `table_exists` Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By changing the comparison to use lowercase versions of the table name and the output, we ensure that the comparison is case insensitive, resolving the issue reported in the failing test and GitHub.