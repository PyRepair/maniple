## Bug Explanation
The bug in the `table_exists` function lies in the conditional check that determines the existence of a table when a partition is provided. When a partition is specified, the function incorrectly constructs the Hive command to check for the existence of the table with that partition. However, the constructed Hive command is flawed in formatting the `show partitions` query, leading to incorrect results.

## Bug Fix Strategy
To fix the bug, we need to ensure that the Hive command for checking the existence of a table with a specified partition is correctly formatted. This involves constructing a valid Hive query that accurately reflects the table and partition being checked.

## Corrected Code
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        partition_query = ' AND '.join(['{}="{}"'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2});'.format(database, table, partition_query))
        return stdout and len(stdout.strip()) > 0
```

This corrected version ensures that the Hive command for checking the existence of a table with a specified partition is properly formatted, allowing for accurate verification of the table's existence.