### Analysis:
1. The `table_exists` function is supposed to check if a given table exists in the specified database with optional partition information.
2. The function calls `run_hive_cmd` to execute the Hive command.
3. The bug seems to be related to the condition checks and the handling of the command output.
4. The expected behavior is to return `True` if the table exists, otherwise `False`.

### Bug:
The bug lies in the condition checks after running the Hive command. The function is not correctly evaluating the output of the command.

### Fix:
We need to ensure that the function correctly handles different scenarios based on the output of the Hive command.
1. Check for the presence of the table name in the command output to determine if the table exists.
2. Modify the function to return `True` if the table exists and `False` otherwise.

### Corrected Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return table in stdout.splitlines() if stdout else False
    else:
        stdout = run_hive_cmd(f"use {database}; show partitions {table} partition ({self.partition_spec(partition)})")

        return True if stdout else False
```

By splitting the stdout by lines, we can check if the table name exists in the list of tables returned by the command. Also, we simplify the return statements to return `True` or `False` based on the command output.