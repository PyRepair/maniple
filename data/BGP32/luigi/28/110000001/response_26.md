The bug in the function `table_exists` is that the `partition` parameter is not being correctly handled in the else block. The `stdout` variable is being assigned the result of running a Hive command using `run_hive_cmd`, but the conditional check for its value does not evaluate the presence of the table in the stdout output.

To fix this bug, the corrected version of the function would need to properly handle the partition parameter and check for the existence of the table based on the stdout output.

Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd(
            'use {0}; show tables like "{1}" partition ({2});'.format(database, table, self.partition_spec(partition))
        return stdout and table in stdout
``` 

In this corrected version, the Hive command to check the existence of the table with a specified partition has been modified. The format and usage of the `run_hive_cmd` function are adjusted to properly handle the partition parameter and check for the existence of the table in the stdout output.