### Bug Explanation
The bug in the `table_exists` function arises from how the function checks for the existence of a table in the database. When a partition is provided, the function constructs a command that includes the partition information, but the way the function is checking the return value of the command is not handling it correctly.

In the first case, the `stdout` variable contains the string `'OK'`, but the function is checking for an exact match with the `table` variable. This leads to a false negative result.

In the second case, the `stdout` variable contains `'OK\nmytable'`, but the function is looking for an exact match with the `table` variable, which causes another false negative result.

The bug occurs because the function is not correctly parsing the output of the Hive command to determine if the table exists in the database.

### Bug Fix Strategy
To fix the bug, we need to modify how the function checks the output of the Hive command when verifying the existence of a table. Instead of looking for an exact match, we should check if the `table` name appears in the output. This will accommodate cases where extra information is returned along with the table name.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd('use {0}; show tables like "{1}" partition ({2});'.format(database, table, self.partition_spec(partition)))

        return stdout and table in stdout
``` 

In the corrected version, the function checks if the `table` name is present in the `stdout` variable, allowing for partial matching instead of exact matching to determine the existence of the table.