### Bug Explanation:
The bug in the `table_exists` function occurs due to the inconsistency in checking for the existence of a table in the Hive database. When checking for the table's existence without a partition, the function uses `"show tables like"` which returns a list of tables separated by new lines. In that case, the function checks if the `table` string is in the output. However, when checking for a table with a partition, the function uses `"show partitions"` which returns multiple partitions with the table name if it exists. Hence, the current implementation does not handle the case properly where the `table` might be part of multiple partitions.

### Bug Fix Strategy:
To fix the bug, we need to update the logic of the `table_exists` function to handle both cases consistently. We should check if the `table` is present in the stdout regardless of whether partitions are specified or not.

### Updated/Created Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s""" % (database, table))

        return table in stdout
``` 

This updated function will check if the `table` is present in the `stdout` regardless of whether partitions are specified or not, ensuring consistent behavior in determining the existence of the table in the Hive database.