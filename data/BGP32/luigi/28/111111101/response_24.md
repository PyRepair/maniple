### Bug Explanation
The bug in the `table_exists` function arises from the conditions used to determine if a table exists or not. When checking if the table exists without a partition, the function looks for an exact match of the table name in the output. However, when a partition is specified, the function calls `partition_spec` to get the partition information but does not properly handle the output comparison, leading to incorrect logic.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly handles the comparison of the output when checking for the existence of a table with or without a partition. The comparison should account for both scenarios to accurately determine if the table exists.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    stdout = ""
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    else:
        partition_value = self.partition_spec(partition)
        stdout = run_hive_cmd("use {}; show partitions {} partition ({});".format(database, table, partition_value))

    return bool(stdout)
```

By updating the `table_exists` function to the corrected version above, we handle both cases of checking for table existence accurately. This fix ensures that the function returns `True` if the table exists based on the `stdout` output and `False` otherwise.