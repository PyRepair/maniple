### Bug Explanation
The bug in the `table_exists` function is related to how the function checks if a table exists in Hive. In the case where the `partition` parameter is `None`, the function executes a Hive command to show tables like the specified table name and then checks if the table exists in the output. However, the bug arises from the condition `return stdout and table in stdout`. The issue is that when the `stdout` contains the table name, the condition `table in stdout` will always evaluate to `True`, causing the function to return `True` even when the table does not exist.

### Bug Fix Strategy
To fix the bug, we need to change the condition that checks if the table exists in the output. Instead of checking if the table name is in the output text, we should check if the table name is on a separate line in the output. This will ensure that only exact matches are considered as the table existing.

### Corrected Version of the Function
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

By splitting the `stdout` text into lines and checking if the table exists on a separate line, we ensure that the function only returns `True` when the exact table name is found in the output.