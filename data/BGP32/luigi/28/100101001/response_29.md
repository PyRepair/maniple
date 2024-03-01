### Analysis:
The `table_exists` function is supposed to check whether a table exists in a database. However, the function is not correctly parsing the output of the `run_hive_cmd` function to determine table existence.

### Bugs:
1. The function is not properly handling the case where the table name matches a substring in the output, leading to incorrect results.
2. The function is not accounting for case insensitivity when comparing table names.

### Bug Fix Strategy:
1. Update the function to check if the table name is a full match to avoid partial matches.
2. Convert both table names to lowercase before comparison to handle case insensitivity issues.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.strip, stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))

        return table.lower() in map(str.strip, stdout.split('\n'))
```

By making the above corrections, the function should now properly handle table existence checks and pass the failing tests, ensuring that tables are accurately detected in the Hive database.