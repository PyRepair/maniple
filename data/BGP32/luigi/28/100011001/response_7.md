### Bug Explanation
The buggy function `table_exists` is failing to correctly determine if a table exists in the given database. The bug is caused by the `if stdout:` condition checking that the `stdout` variable is not empty to determine if the table exists. In the failing tests, the function is returning False even when the table does exist, leading to the assertion errors.

The issue lies in the fact that the condition `if stdout:` will evaluate to False if `stdout` is a non-empty string (like "OK\nmytable"), as it's considered truthy in Python. Therefore, the function wrongly returns False when the table is indeed found in the database.

### Bug Fix Strategy
To fix this bug, we need to adjust the conditions properly to check if the exact table name exists in the `stdout` variable. We also need to handle cases where the table name is not found correctly.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split()
    else:
        cmd_output = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        return table in cmd_output.split()
``` 

By splitting the stdout and checking for the presence of the exact table name in the list created by splitting the stdout, we ensure that the function correctly identifies if the table exists in the database.