### Bug Explanation
The bug in the `table_exists` function is due to the logic in the `if` statements. In the first case where there is no partition specified, the function checks if the table name is present in the output of the `run_hive_cmd` function. However, the bug arises because the function only checks if the stdout is not empty, which results in `True` even if the table name is not found in the output.

In the second case where a partition is specified, the function checks if the `stdout` variable is not empty to return `True`, regardless of the actual content of the `stdout`.

### Fix Strategy
To fix the bug, we need to check if the table name is present in the output of the `run_hive_cmd` function, not just if the output is not empty. Additionally, when checking for partitions, we need to verify if the table name and partition are present in the `stdout` variable.

### Corrected Version
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout and table in stdout
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
            return all(x in stdout for x in [table, self.partition_spec(partition)])
``` 

By modifying the return statements to check if the table name is present in `stdout` for both cases, we ensure that the function correctly determines if a table exists regardless of the presence of other output in the `stdout` variable.