The issue in the buggy function lies in the condition checking. When checking if a table exists, the current implementation returns the opposite value of what is expected. Therefore, the bug can be fixed by correcting the return statements in the `table_exists` function.

Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return stdout or False
```

By fixing the return statements within the `table_exists` function, the corrected version will now pass the failing test cases and the corresponding error messages provided above.