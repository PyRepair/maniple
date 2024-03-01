### Analysis:
1. The function `table_exists` in the `hive.py` file is intended to check if a specified table exists in a given database with an optional partition.
2. The bug seems to be related to the conditional check in the function.
3. The failing test cases indicate that the function is returning incorrect results when checking the existence of tables.
4. The bug appears to be in the conditional return statements of the function, causing incorrect boolean evaluations.
5. To fix the bug, we need to modify the conditional checks in the function to ensure the correct evaluation of table existence.

### Bug Fix:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout.split('\n')[1:]
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
```

By splitting the `stdout` variable with `'\n'` in the first case and directly returning the boolean evaluation of `stdout` in the second case, we ensure that the function correctly detects the existence of tables in the database.

This fix should address the bug and make the function pass the failing test cases.