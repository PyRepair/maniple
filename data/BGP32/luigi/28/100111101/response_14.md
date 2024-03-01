### Bug Explanation
The bug in the `table_exists` function is due to the incorrect check on the presence of the table in the `stdout`. The function currently checks if `stdout` exists and if the `table` string is in it, which is not accurate because `stdout` could contain other strings besides the table name.

### Bug Fix Strategy
To fix the bug, we need to modify the condition checks in the function to accurately determine the presence of the table name in the `stdout`.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))
        return any(table == t for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd('use {0}; show tables like "{1}" partition ({2});'.format(database, table, self.partition_spec(partition)))
        return any(table == t for t in stdout.split('\n'))
```

In this corrected version:
- For the case when partition is None, we run `show tables` to get a list of all tables and then check if the `table` is in that list.
- For the other case, we run `show tables like "{table}" partition ({partition})` to display tables that match the specified partition conditions and then check if the `table` is in that list.

This approach ensures a more accurate check for the existence of the specific table in the output.