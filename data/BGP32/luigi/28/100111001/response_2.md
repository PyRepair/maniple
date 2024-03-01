### Bug Explanation
The bug in the `table_exists` function lies in the logic to check if a table exists in the database. In the `stdout` variable check, the function is not properly handling the case where the table name might be present in a newline-separated string. This is evident from the failing test cases where the function fails to correctly identify the table existence when the table name is part of a newline-separated string in the `stdout`.

### Bug Fix Strategy
To fix the bug, we need to modify the logic in the function to properly handle the case where the table name is in a newline-separated string.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` on the newline character (`\n`), we can properly check if the table name exists in the returned string. This should fix the bug and make the function correctly identify table existence.