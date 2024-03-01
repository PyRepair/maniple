### Analysis:
The error message indicates that the test case `test_table_exists` and `test_apacheclient_table_exists` are failing because the assertion `self.assertTrue(returned)` is failing. This means that the function `table_exists` is returning incorrect results.

### Potential Error Locations:
1. The condition for checking the existence of a table without a partition.
2. The condition for checking the existence of a table with a partition.

### Cause of the Bug:
1. For the condition without a partition, the function is not correctly handling the output of the `run_hive_cmd` function. It is not checking if the table exists in the output.
2. For the condition with a partition, the function is not correctly formatting the command to check for partitions.

### Strategy for Fixing the Bug:
1. Check the output of `run_hive_cmd` to see if the table exists in the output for the case without a partition.
2. Correctly format the command to check for partitions for the case with a partition specifier.
3. Ensure that the function returns `True` if the table exists and `False` otherwise.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

With this corrected version, the function should now correctly handle the output of the `run_hive_cmd` function and return `True` if the table exists and `False` otherwise. This should fix the failing test cases mentioned above.