### Bug Explanation
The bug in the `table_exists` function lies in the condition checking for the existence of the table in the Hive database. When checking for table existence without a partition specified, the function uses the `show tables like "{1}";` command to retrieve a list of tables. It then checks if the table is in the output, but the comparison is case-sensitive. On the other hand, when a partition is specified, the function uses the `show partitions` command, which may return additional information along with the actual table name, resulting in incorrect comparisons.

### Bug Fix Strategy
To fix the bug, normalize the table names before comparing them to ensure case-insensitive matching. Also, when a partition is specified, extract just the base table name from the output of the `show partitions` command before comparison.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    normalized_table = table.lower()  # Normalize table name for case-insensitive comparison
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and normalized_table in stdout.lower()
    else:
        partition_base_table = table.split('.')[0]  # Extract the base table name from the partition spec
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return normalized_table == partition_base_table
        else:
            return False
``` 

By normalizing table names and extracting the base table name when dealing with partitions, the corrected version of the function ensures proper table existence checks in a case-insensitive manner and handles partitioned tables correctly.