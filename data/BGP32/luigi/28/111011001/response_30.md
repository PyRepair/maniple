### Analysis:
1. The `table_exists` function in the `HiveCommandClient` class is supposed to check if a table exists in a given database, with an optional partition specification.
2. The function uses `run_hive_cmd` function to run Hive commands and check the output to determine the existence of the table.
3. The bug seems to be in the comparison logic of the returned `stdout` which is not handling the cases correctly. The bug is likely caused by the way the function checks the existence of the table in the stdout.
4. To fix the bug, we need to adjust the logic of how the function checks the existence of the table in the stdout.

### Bug Fix Strategy:
- We need to modify the logic to properly check for the existence of the table in the `stdout` returned from the `run_hive_cmd` function.
- We need to handle cases where the table name is present in the `stdout`.
- In the current implementation, the function is not correctly handling the comparison with `stdout` which leads to incorrect results.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
        return "OK" in stdout
```

The corrected version above changes the logic of the return statement to properly check if `"OK"` exists in the `stdout` returned from the `run_hive_cmd` function. This adjustment ensures that the function correctly identifies the existence of the table based on the output received.