The bug in the `table_exists` function is related to how the output of the `run_hive_cmd` function is handled. The function is checking whether a table exists in a specific database and partition in Hive. The issue arises when checking the output of the `run_hive_cmd` function and determining if the table exists based on this output.

The bug is caused by how the condition for checking if the table exists is implemented. In the case where no partition is provided, the condition `return stdout and table in stdout` is used to determine table existence, which is incorrect. The `run_hive_cmd` function may return 'OK', which would lead to the condition evaluating to `True` when it is expected to be checked using a table name. 

To fix this bug, the `table_exists` function should check if the table name is present in the output of the `run_hive_cmd` function, instead of solely relying on the truthiness of the output.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
        return table in stdout.split('\n')
```

In this corrected version, the output of the `run_hive_cmd` function is split by newline characters (`\n`), allowing the function to correctly check if the table name exists in the list of tables returned.

This fix should resolve the bug and ensure that the `table_exists` function behaves as expected when checking for the existence of a table in Hive.