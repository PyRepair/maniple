The bug in the `table_exists` function lies in the logic of checking if the table exists in the given Hive database. The function is not correctly parsing the output of the `run_hive_cmd` function to determine if the table exists or not. This is causing the test cases to fail.

To fix the bug, we need to modify the logic for checking the existence of the table in the given database. We should check if the table name is present in the output of `run_hive_cmd` to determine if the table exists or not.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
```

With this corrected version, the function should now correctly check if the table exists in the database based on the output of the `run_hive_cmd` function.

The provided test cases should now pass with this corrected version of the function.