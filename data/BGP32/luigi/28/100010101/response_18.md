### Analysis
1. The buggy function is intended to check if a table exists in a Hive database. It uses the `run_hive_cmd` function to execute Hive commands and then checks if the table exists based on the output.
2. The bug seems to be related to how the function handles the stdout from the `run_hive_cmd` function.
3. The bug occurs because the function is not correctly checking the presence of the table in the stdout. It returns `False` when it should return `True` for existing tables.
4. To fix the bug, the function should properly parse the output from `run_hive_cmd` and check if the table name is present in it.
5. The corrected version will handle both cases where tables exist or don't exist in the specified database.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By using the `bool()` function on the stdout, we convert any non-empty string to `True` (indicating the table exists) and empty string to `False` (indicating the table doesn't exist). This modification ensures that the correct boolean value is returned based on the presence of the table in the database.