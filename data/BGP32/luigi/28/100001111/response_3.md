The bug in the provided function `table_exists` is that it does not account for case sensitivity when checking if a table exists in Hive. To fix this bug, we need to modify the comparison between the table name and the output from Hive to be case insensitive.

Here is the corrected version of the function:

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

In the corrected version, we convert both the table name and the output from Hive to lowercase before performing the comparison, making the check case insensitive. This change aligns with the issue reported on GitHub and resolves the reported bug effectively.