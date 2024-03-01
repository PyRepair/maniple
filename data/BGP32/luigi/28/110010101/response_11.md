### Analysis
The `table_exists` function in the `HiveCommandClient` class is designed to check if a given table exists in a Hive database. However, there are issues with the implementation that lead to failing test cases. 

### Bug
1. In the first case, where only the table parameter is provided, the function only checks if the table name is present in the stdout string. The current implementation erroneously returns True if the table name matches anywhere in the output and False if it doesn't.
2. In the second case, where both the database and table parameters are provided, the function tries to check for partitions based on the provided partition, but the partition specification is incorrect.
3. The function should distinguish between the table name case sensitivity to match the expected table names.

### Bug Fixes
1. Update the `stdout` check to ensure that the exact table name is found in the list of tables.
2. Properly format the query to check for partitions.
3. Normalize the table name casing for proper evaluation.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return any(table.lower() == t.lower() for t in stdout.split())
    else:
        partition_query = ' and '.join('{} = \'{}\''.format(k, v) for k, v in partition.items())
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                                ({2})""".format(database, table, partition_query))

        return bool(stdout)
``` 

The corrected version ensures proper table existence checks and partition checks in a case-insensitive manner, fixing the issues identified.