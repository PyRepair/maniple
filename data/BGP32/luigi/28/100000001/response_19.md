## Analysis:
1. The function `table_exists` is designed to check if a table exists in a specified database with an optional partition.
2. There seems to be an issue with the way the Hive commands are constructed and executed in both the `if` and `else` blocks.
3. The `run_hive_cmd` function is used to execute Hive commands, but the way the commands are formatted could potentially lead to errors.

## Bug Explanation:
The bug in the function lies in the way the Hive commands are constructed and executed:
1. In the `if` block, the Hive command for checking table existence is correct, but the variable `stdout` may not capture the output correctly due to how the `run_hive_cmd` function is called.
2. In the `else` block, the Hive command for showing partitions is incorrect due to the incorrect formatting of the command string.

## Bug Fix Strategy:
1. Ensure proper formatting and execution of the Hive commands in both the `if` and `else` blocks.
2. Make sure that `run_hive_cmd` function returns the output of the command execution.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd(f'use {database}; show tables like "{table}";')
        return stdout.strip() == table
    else:
        stdout = run_hive_cmd(f'use {database}; show partitions {table} partition ({self.partition_spec(partition)});')
        return len(stdout.strip()) > 0
```