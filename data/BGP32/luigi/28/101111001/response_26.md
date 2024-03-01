### Bug Explanation:
The bug in the `table_exists` function lies in the condition where the `table` variable is checked within the `stdout` output as a substring. The function checks if the `table` string is in the `stdout` as a whole, instead of checking for a specific table name in the list of tables obtained from the `show tables` command.

### Bug Fix Strategy:
To fix the bug, we need to modify the logic of checking if the `table` exists in the list of tables. We should split the `stdout` into lines and check if the `table` string exists on one of those lines instead of just the whole `stdout` string.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        tables = stdout.split('\n')[1:]  # Skip the first line as it's a header
    
        return any(t.strip() == table for t in tables)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` into lines and checking if the `table` string exists in one of those lines, we ensure that the function correctly determines if a table exists in the database, resolving the bug.