### Bug Explanation
The bug in the `table_exists` function lies in the conditional check that determines whether the table exists in the database. In the first if block, the condition `return stdout and table in stdout` will only return `True` if both `stdout` is not empty and the exact table name is found in `stdout`. This condition is causing the first failing test to fail even when the table exists.

In the second if block, the `stdout` variable is checked directly for truthiness, which may not accurately reflect whether the table exists or not. This check leads to the second failing test to fail as well.

### Bug Fix Strategy
1. Modify the condition in the first if block to check if the table name is in the list of tables returned by the `show tables` command.
2. Modify the condition in the second if block to check if the `stdout` contains the partition information.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables;'.format(database))

        return stdout and table in stdout.splitlines()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By splitting `stdout` into lines in the first if block and directly returning the truthiness of `stdout` in the else block, the corrected version addresses the issues causing the failing tests.