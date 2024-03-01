The bug in the `table_exists` function is due to a case sensitivity issue when checking if the table exists in Hive. The function compares the table name directly with the output from Hive, which can cause problems if the case of the table name does not match exactly with the output from Hive. 

To fix this bug, we need to make the comparison case insensitive by converting both the table name and the output from Hive to lowercase before comparing them.

Here is the corrected version of the `table_exists` function:

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

This corrected version ensures that the comparison between the table name and the output from Hive is case insensitive, fixing the bug reported in the GitHub issue. Now the function should work as expected for case-insensitive table existence checks.