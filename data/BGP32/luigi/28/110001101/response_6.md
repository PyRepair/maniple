### Bug Explanation
The bug in the `table_exists` function occurs due to the check on the `stdout` variable in the `if` conditions. The function checks if `stdout` contains the table name in two different ways - using `table in stdout` and directly checking if `stdout` exists. This can lead to inconsistent results. Additionally, in the case where a `partition` is provided, the query being executed to check the table's existence is incorrect.

### Bug Fix Strategy
To fix this bug, we need to ensure that the function consistently checks if the table exists based on the `stdout` variable and modify the query being run when a partition is provided.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2});""".format(database, table, self.partition_spec(partition)))
    
        return stdout is not None
```

In the corrected version, we consistently check if `stdout` exists or not to determine if the table exists. Additionally, the query to check for the existence of a partitioned table is fixed to ensure that the correct query is executed.