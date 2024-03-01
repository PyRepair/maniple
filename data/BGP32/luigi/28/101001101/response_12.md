### Bug Explanation
The bug in the `table_exists` function arises from the logic used to check for the existence of a table in a database, especially when dealing with partitions. In the `else` block of the function, the query constructed to check for partitioned tables is incorrect. It does not handle the partition correctly, resulting in an incorrect evaluation of the table existence.

### Bug Fix Strategy
To fix the bug, we need to correctly construct the query to check for the existence of partitioned tables and handle the partition information accurately.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        # changed to properly handle partitions
        partition_str = ','.join(["{}='{}'".format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("use {}; show partitions {} ({})".format(database, table, partition_str))

        if stdout:
            return True
        else:
            return False
```

By constructing the `partition_str` accurately using the `partition` dictionary and incorporating it correctly into the query to check for partitioned tables, the corrected function should now properly handle table existence checks for partitioned tables as well.