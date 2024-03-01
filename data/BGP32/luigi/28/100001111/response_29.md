The bug in the provided function arises from the case sensitivity during table existence checks in Hive. The function is case-sensitive, which causes it to fail when there are discrepancies between the table names in different cases. To fix this, the function needs to compare the table name in a case-insensitive manner with the output from Hive.

### Strategy for fixing the bug:
- Modify the function to compare table names in a case-insensitive way by converting both the table name and the output from Hive to lowercase.
- Check if the lowercase table name exists in the lowercase output from Hive to determine the table's existence accurately.

### Corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table.lower()))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By converting both the table name and the output to lowercase before comparison, this corrected function ensures a case-insensitive check for table existence. This fix addresses the issue reported on GitHub, making the `table_exists` function more robust and suitable for handling table names in different cases.