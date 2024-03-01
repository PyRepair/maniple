## Bug Analysis

The bug in the `table_exists` function is likely related to how the function checks for the existence of a table. In the first part of the function, it runs a hive command to show tables like the input table name. If the table exists, it should return `True`, but the current implementation checks if the table name is in the output string, which can result in false positives if the table name is a substring of another table name.

In the second part of the function, when a partition is provided, it tries to show partitions for a specific partition spec. The bug here might be in the construction of the hive command, which may not be correctly formatted.

## Bug Fix Strategy

To fix the bug, we need to modify the logic in the `table_exists` function to accurately check for the existence of the specified table. When checking tables without partitions, we should parse the output of the `show tables` command properly to ensure that the table name matches exactly. When dealing with partitions, the construction of the hive command needs to be revised to correctly query for partitions.

## Corrected Version

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables in {1} like "{2}";'.format(database, database, table))

        return stdout and table in stdout.split()
    else:
        partition_str = ', '.join(['%s="%s"' % (k, v) for k, v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_str))

        return stdout is not None and len(stdout.strip()) > 0
```

In the corrected version:
- The `show tables` command now explicitly shows tables in the specified database to avoid false positives.
- The `partition_str` is constructed correctly for querying partitions, and we check if the output is not empty to determine if the partition exists.