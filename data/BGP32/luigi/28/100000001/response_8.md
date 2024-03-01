## Analysis:
1. The function checks if a table exists in a Hive database by running the `show tables like` command for a non-partitioned table and `show partitions` command for a partitioned table.
2. There are potential errors in the format of the Hive commands being constructed in the code.
3. The bug in the code is due to incorrect indentation and formatting of the `run_hive_cmd` commands within the `if` and `else` blocks.
4. To fix the bug, we need to properly format the Hive commands in the `if` and `else` blocks and ensure they are correctly concatenated before executing them.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd(
            'use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show partitions {1} partition ({2})'.format(database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

In the corrected version:
1. The indentation of `run_hive_cmd` commands in both `if` and `else` blocks is corrected.
2. The Hive commands are now formatted using `.format()` method for easier readability and maintenance.
3. The `if` block now checks for the presence of the table name in the stdout of `show tables like` command.
4. The `else` block executes the `show partitions` command with proper formatted syntax using `.format()` method.
5. Boolean conversion of `stdout` is done before returning the result.