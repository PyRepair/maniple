### Bug Explanation
In the `table_exists` function, the bug occurs due to the incorrect usage of the `run_hive_cmd` function. The function calls `run_hive_cmd` to check if a table exists in a database by running a Hive query. However, in the case where a `partition` is provided, the function incorrectly constructs the query string using `self.partition_spec(partition)` without considering the actual structure of the `partition` parameter. This leads to the query being malformed and not executing correctly.

### Bug Fix Strategy
To fix the bug, we need to ensure that the query string is constructed correctly when a `partition` is provided. This involves examining the structure of the `partition` parameter and appropriately formatting it within the Hive query.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        partition_values = ','.join(['{0}="{1}"'.format(k, v) for k, v in partition.items()])
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                            ({2})""".format(database, table, partition_values))

        if stdout:
            return True
        else:
            return False
``` 

This corrected version of the function properly constructs the query string when a `partition` is provided, concatenating the key-value pairs of the `partition` dictionary into the proper format for the Hive query.