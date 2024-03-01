### Analysis
1. The buggy function `table_exists` checks if a table exists in a Hive database using the `run_hive_cmd` function.
2. The bug seems to be related to how the function compares the stdout output from the `run_hive_cmd`.
3. The bug occurs when the function checks if the table name is present in the stdout. It is failing to correctly detect the table name due to the formatting of the stdout.
4. To fix the bug, we need to modify how the function processes the stdout to correctly identify the table name.

### Bug Fix
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return stdout and table in stdout.split()
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition ({2})""".
                            format(database, table, self.partition_spec(partition)))

        if stdout:
           return True
        else:
           return False
```

### Explanation
1. The fix involves modifying the query to `show tables;` instead of `show tables like "{1}";` to get a list of all tables in the database.
2. The function now splits the stdout into a list of table names using `split()` and checks if the table exists in that list.
3. This fix ensures that the function can correctly detect the presence of the table in the list of tables returned by the command.
4. By addressing the stdout formatting issue, the corrected function should now pass the failing tests and satisfy the expected input/output values.