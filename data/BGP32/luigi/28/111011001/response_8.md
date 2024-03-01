### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in a specific database.
2. The bug seems to be in the comparison logic of the function where it checks if the table is in the output of the `run_hive_cmd` function.
3. The bug occurs because the function is checking for an exact match between the table name and the output, but the output may contain additional information (like table names of existing tables).
4. The strategy to fix the bug is to modify the comparison logic to make sure that the table name in the output is a complete match rather than just a substring check.

### Bug Fix:
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split()

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

In the corrected version, now the function splits the output of `run_hive_cmd` by whitespace and then checks if the table name is in the list of table names. This should ensure that the function correctly identifies the existence of a specific table.