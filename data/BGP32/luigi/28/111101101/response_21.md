### Bug Explanation
The bug lies in how the function `table_exists` is checking if the table exists. In the `if partition is None` case, the function is only checking if the table name is in the stdout, which is incorrect. It should instead check if the table name is in the lines of stdout. In the case where `partition` is not None, the function is not building the query correctly to check for the existence of a partition. Additionally, it is not checking if the partition exists in the stdout.

### Bug Fix Strategy
1. Adjust the logic in the `if partition is None` case to check if the table name is in the lines of stdout.
2. Fix the query building in the `else` case to correctly check for the existence of a partition.
3. Verify that the partition exists in the stdout while checking for partitions.

### Corrected Function
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table in stdout.split('\n')
        else:
            partition_query = ','.join(f"{k}='{v}'" for k, v in partition.items())
            query = "use {0}; show partitions {1} ({2})".format(database, table, partition_query)
            stdout = run_hive_cmd(query)
    
            return partition_query in stdout
``` 

After applying these changes, the corrected `table_exists` function should pass all the failing tests provided.