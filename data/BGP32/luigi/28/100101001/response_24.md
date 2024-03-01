### Analysis:
The buggy function `table_exists` is supposed to check if a table exists in a given database, with an optional partition. The function uses the `run_hive_cmd` function to execute Hive commands and check the output for the existence of the table.

From the failing test cases, we can see that the function is incorrectly handling the stdout from the `run_hive_cmd` function. The function expects the output to contain the table name for existence validation, but it is not processing the stdout correctly in all cases.

### Bug:
The bug occurs because the function does not properly parse the stdout from the `run_hive_cmd` function. In the cases where the function is expected to return `True` for table existence, it fails because it does not handle the stdout output correctly.

### Strategy for fixing the bug:
1. Modify the function to properly process and parse the stdout from the `run_hive_cmd` function.
2. Ensure that the function correctly checks for the table name in the stdout output to determine the existence of the table.
3. Handle both cases when a partition is specified and when it is not.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        partition_str = self.partition_spec(partition)
        stdout = run_hive_cmd('use {0}; show partitions {1}.{2} partition ({3});'.format(
            database, database, table, partition_str))

        return 'OK' in stdout
```

In the corrected version of the function:
- For the case where a partition is specified, we construct the proper Hive command using the partition information and then check if 'OK' is in the stdout output to determine table existence.
- The function now properly handles the stdout output to validate the table existence in both cases.