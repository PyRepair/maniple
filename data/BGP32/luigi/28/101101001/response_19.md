### Bug explanation:
The bug in the `table_exists` function lies in the condition to check if the `table` exists in the `stdout` output after running the Hive command. The condition `return stdout and table in stdout` is incorrectly implemented because it checks if `stdout` is not empty (`stdout`) and if `table` is a substring of `stdout`, which may result in unexpected behavior.

### Bug fix strategy:
To fix the bug, we need to modify the condition to check if `table` is an exact match in the retrieved tables rather than being a substring. This will ensure the correct evaluation of whether the specified table exists in the database.

### Corrected version of the function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table).lower())

        tables = stdout.strip().split('\n')
        return table.lower() in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By modifying the condition and handling the table retrieval correctly, we ensure that the function correctly identifies whether a table exists in the specified database. This corrected version should now pass the failing test cases.