### Identified Bug:
The bug in the `table_exists` function is caused by the comparison of the table name in a case-sensitive manner, leading to test failures when the case of the table name doesn't match exactly with the output from the Hive command. The function needs to make the comparison case-insensitive to address this issue.

### Suggested Fix Strategy:
To fix the bug, modify the comparison of the table name from `table in stdout` to `table.lower() in stdout.lower()` to make it case-insensitive.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By making this change to the `table_exists` function, the comparisons will be done in a case-insensitive manner. This correction aligns with the suggested fix mentioned in the GitHub issue #896 related to making the `table_exists` function case-insensitive.