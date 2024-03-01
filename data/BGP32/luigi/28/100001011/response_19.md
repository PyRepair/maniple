The buggy function `table_exists()` in the provided code is causing issues due to case sensitivity when checking for table existence in Hive. The function compares the table name directly to the output from Hive, leading to failures when the cases do not match.

The fix involves converting both the table name and the output from Hive to lowercase for comparison, thus making the check case-insensitive.

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

With this correction, the function will compare the lowercase versions of both the table name and the Hive output, resolving the case sensitivity issue reported in the GitHub issues.