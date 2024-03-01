### Bug Explanation:
The buggy function `table_exists` has a problem with how it checks for the existence of a table. The function checks the output of the `run_hive_cmd` function and compares it with the table name to determine if the table exists. The issue arises because of how the function is checking the presence of the table in the output; it does a simple string check which can lead to incorrect results.

In the failing test cases, when the table name is present in the output of `run_hive_cmd`, the function should return `True`. However, the implementation of the function currently looks for an exact match of the table name without considering the format of the output from `run_hive_cmd`, leading to false negatives.

### Bug Fix Strategy:
To fix the bug in the `table_exists` function, we should modify the logic to properly parse the output of `run_hive_cmd` and check if the table name is present in the output. Instead of a simple string check, we need to split the output by newlines and then search for the table name in the resulting list of table names. This approach will ensure that we correctly identify the presence of the table in the output regardless of the format.

### Corrected Version of the Function:
```python
# Fixing the buggy function to correctly check for the existence of a table
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        if stdout:
            return any(t.strip() == table for t in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
        if stdout:
            return True
    return False
```

By splitting the `stdout` by newlines and then checking if any table name in the list matches the provided table, we ensure a more robust way of verifying the existence of the table. This corrected version should now pass the failing test cases.