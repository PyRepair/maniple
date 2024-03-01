### Analysis
1. The buggy function checks if a table exists in a specified database by running a command in Hive.
2. The function fails to correctly handle the output from the `run_hive_cmd` function.
3. The bug is related to how the function checks the existence of the table based on the stdout output from the `run_hive_cmd`.
4. The strategy to fix the bug is to properly parse the stdout output from the `run_hive_cmd` function to determine the existence of the table.

### Bug Fix
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))

        return any(partition in line for line in stdout.split("\n"))
```

By splitting the `stdout` output and then checking if the `partition` is present in any of the lines, we can correctly determine the existence of the table when checking for partitions.

This corrected function should now fulfill all the expected test cases and correctly identify the existence of tables in the specified database.