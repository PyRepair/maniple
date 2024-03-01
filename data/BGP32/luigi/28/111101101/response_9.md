### Fixing the Bug:
The bug in the `table_exists` function is caused by the condition `stdout and table in stdout`. The function should be checking if the table name exists in the stdout rather than just checking if stdout exists. Additionally, the function should check for case insensitivity when comparing the table names.

To fix the bug, the function should be modified to check if the table name is present in stdout regardless of case. This can be achieved by converting both the table name and the stdout to lowercase before comparing them.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("use %s; show partitions %s partition (%s)" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By making the table name and the stdout lowercase before comparison, the function will correctly check if the specified table exists in the stdout output, thus fixing the bug identified in the failing tests.