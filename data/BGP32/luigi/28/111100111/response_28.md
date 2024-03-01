The bug in the `table_exists` function is that it only checks if the table name exists in the output from the `run_hive_cmd` function without considering case sensitivity. This leads to discrepancies when comparing table names with different cases. To fix this bug, we need to make the comparison case insensitive by converting both the table name and the output to lowercase.

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

By converting both the table name and the output to lowercase before comparison, the function will be able to correctly identify the existence of a table regardless of the case used in the table name.

This corrected version should pass all the failing test cases provided.