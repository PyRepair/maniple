The issue with the `table_exists` function is that it checks for exact table name matches in the Hive output, without considering cases. This causes issues when checking for tables with different case formats.

To fix this bug, we can modify the function to convert both the table name and the Hive output to lowercase before performing the match, making the check case insensitive.

Here is the corrected code for the `table_exists` function:

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

With this fix, the `table_exists` function should correctly compare table names in a case-insensitive manner and resolve the issue posted in GitHub.