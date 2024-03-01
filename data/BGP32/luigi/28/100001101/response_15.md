### Bug Explanation:
The bug in the `table_exists` function arises due to the incorrect comparison of the `table` name with the `stdout` result. The function is checking if the table name is contained in the `stdout` output, which can lead to false positives or negatives. For example, in Case 2, the function incorrectly detects the table name `'mytable'` within the output `'OK\nmytable'`. This can result in incorrect behavior when determining whether a table exists or not.

### Bug Fix Strategy:
To fix the bug, the function should explicitly check if the table name is an exact match within the `stdout` output. This will ensure more accurate results when determining if a table exists in the database.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split()

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

After applying this correction, the function will return a boolean value based on whether the table name is an exact match in the `stdout` output, ensuring correct behavior when checking for table existence.