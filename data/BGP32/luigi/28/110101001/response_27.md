### Bug Explanation:
The bug in the `table_exists` function lies in the logic of checking if the table exists in the output of the `run_hive_cmd` function. The current implementation checks if the table name is in the entire output string, which can lead to false positives if the table name is a substring of another table name in the output. This is evident in the failing test cases where the function incorrectly identifies the table existence.

### Bug Fix Strategy:
To fix this bug, we should modify the function to check if the table name appears as a separate word in the output (e.g., surrounded by spaces or newlines) to ensure an exact match.

### Corrected Version of the `table_exists` function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and f'\n{table}\n' in stdout
    else:
        stdout = run_hive_cmd(f'use {database}; show partitions {table} partition({self.partition_spec(partition)})')
    
        if stdout:
            return True
        else:
            return False
```

By modifying the return statements to check if the table name appears as a separate word in the output with `\n` as the delimiter, we ensure an exact match for the table name existence in the output string. This correction should address the false positives in the failing test cases.