### Analysis:
1. The buggy function `table_exists` is part of the `HiveCommandClient` class in the `luigi/contrib/hive.py` file.
2. The function calls the `run_hive_cmd` function to execute Hive commands.
3. The error message indicates that the test cases for the `table_exists` function are failing.
4. The bug seems to be related to how the function processes the output of the executed commands.

### Issue:
The issue lies in the comparison logic of the `table_exists` function. The function is checking for the presence of the table name in the output of the `run_hive_cmd` function, but the check is not performed correctly.

### Fix:
Modify the logic in the `table_exists` function to properly handle the output of the `run_hive_cmd` function.

### Corrected Version:
```python
class HiveCommandClient(HiveClient):
    """
    Uses `hive` invocations to find information.
    """

    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
            return stdout.strip() == table
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition)))
            return stdout.strip() == table
```

By striping the `stdout` before comparison, the function will now correctly check if the table name is present in the output string.