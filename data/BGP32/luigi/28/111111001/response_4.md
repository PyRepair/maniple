### Bug Explanation:
The bug in the `table_exists` function is due to the check for the table name in the `stdout` output from the `run_hive_cmd` function. The current implementation of the function checks if the table name is in the entire `stdout` output string, which can lead to incorrect results. For example, in Case 2 where the `stdout` is `'OK\nmytable'`, the function incorrectly returns `True` because it finds `table` within the `stdout` string.

### Bug Fix Strategy:
To fix the bug, we need to split the `stdout` string by newline characters (if present) and then check if the `table` name is in the list of table names obtained. This approach will ensure an accurate check for the existence of the table within the `stdout` output.

### Corrected Version of the Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        table_names = stdout.split('\n')
        return table in table_names
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

With this correction, the function will accurately determine if the specified table exists based on the table names obtained from the `stdout` output.