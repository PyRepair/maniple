### Analysis:
1. The function `table_exists` in the `HiveCommandClient` class is checking if a table exists in a given database using Hive commands.
2. The bug seems to be related to how the function processes the output from running the Hive commands.
3. The bug occurs because the function does not handle the case where the table is found in the output from Hive commands properly. It only checks if the `stdout` variable is not empty, which leads to incorrect results.
4. To fix the bug, we need to properly parse the output from Hive commands to check if the specified table exists.

### Bug Fix:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        if stdout:
            return table in stdout
        else:
            return False
    else:
        stdout = run_hive_cmd("""use {}; show partitions {} partition({})""".format(database, table, self.partition_spec(partition)))
        if stdout:
            return True
        else:
            return False
```

By properly checking if the `table` exists in the `stdout`, we ensure that the function returns the correct results in all scenarios.