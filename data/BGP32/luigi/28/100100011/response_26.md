The bug in the `table_exists` function is that it is not case insensitive when checking for table existence. This causes an issue when comparing table names in different cases, as Hive is case-insensitive and returns table names in lowercase. The fix involves converting both the table name and the stdout to lowercase for comparison.

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

By converting both the table name and the stdout to lowercase before comparison, the function now correctly handles the case-insensitive nature of table names in Hive. This fix should resolve the GitHub issue related to making `table_exists` case insensitive.