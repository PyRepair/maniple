The bug in the `table_exists` function is caused by the incorrect condition checking in the `if` statement. The function currently returns `False` when it should return `True` and vice versa.

To fix this bug, we need to correctly handle the return values from the `run_hive_cmd` function and check if the table exists based on that. Here is the corrected version of the function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return stdout.strip() != ""
```

This corrected version now properly checks for the existence of a table and returns `True` if the output from `run_hive_cmd` is not empty, indicating that the table exists. This should now pass the failing test provided.

Please make this update in the `luigi/contrib/hive.py` file.