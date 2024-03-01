Based on the information provided, the bug in the `table_exists` function is due to a case sensitivity issue when comparing the table name with the output from the Hive command. To fix this bug, we need to convert both the table name and the output to lowercase before comparison.

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

By converting both the table name and the output from the Hive command to lowercase before comparison, we ensure that the function is case insensitive and correctly identifies whether the table exists in the database.

This fix addresses the issue reported on GitHub related to making the `table_exists` function case insensitive.