### Bug Explanation
The bug in the `table_exists` function lies in the comparison of the `stdout` variable after running the `run_hive_cmd` function. In the current implementation, the function checks if `stdout` is not empty and if the `table` is in `stdout`. This logic is incorrect as it doesn't account for cases where the table name might not be an exact match but would still be considered present.

### Bug Fix Strategy
To fix the bug, the comparison logic needs to be modified to consider each line in `stdout` separately and check if any line contains the table name. This way, even if there are multiple lines or additional information in `stdout`, the function can correctly identify the existence of the table.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        if stdout:
            return any(tab.strip() == table for tab in stdout.split('\n'))
        else:
            return False
    else:
        stdout = run_hive_cmd("""
                        use {0};
                        show partitions {1} partition ({2})""".format(database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
```

### Note
In the corrected version, the function splits `stdout` by newline character and then checks if any of the stripped lines match the `table` name. This allows for a more accurate verification of table existence.