### Issues:
1. The function `table_exists` in the `HiveCommandClient` class is not correctly checking for the existence of a table in the Hive database.
2. The function is not handling the case sensitivity of table names properly, leading to a failing test case.

### Cause of the Bug:
The bug is caused by the incorrect check for table existence in the Hive database. When checking if a table exists, the function only compares the table name with the output of the 'show tables' command, which leads to incorrect results, especially when the table names are case-insensitive.

### Bug Fix Strategy:
1. Modify the function to store the output of the 'show tables' command in a list and then compare the table names in a case-insensitive manner.
2. Ensure that the function accounts for the case sensitivity of table names by converting the table names to lowercase before comparison.
3. Modify the function to return `True` if the table is found in the output and `False` otherwise.

### Corrected Version:
```python
class HiveCommandClient(HiveClient):
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables;'.format(database))
            tables = stdout.split('\n')
            return any(t.lower() == table.lower() for t in tables)
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
            return bool(stdout)
```

By implementing the changes above, the function `table_exists` now correctly checks for the existence of a table in the Hive database and accounts for case sensitivity, ensuring that the failing tests pass.