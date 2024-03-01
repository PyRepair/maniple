The buggy function `table_exists` in the `HiveCommandClient` class is failing to handle case insensitivity while checking for table existence in Hive. This bug leads to failing tests in the `hive_test.py` file.

### Potential Error Locations:
1. The comparison between `table` and `stdout` is case sensitive.
2. The function is not handling case insensitivity for table existence checks.

### Cause of the Bug:
The bug arises because the function is directly comparing the table name with the output from the Hive command, which may not match due to case sensitivity.

### Bug Fix Strategy:
To fix the bug, we need to convert both the `table` name and the output `stdout` to either lowercase or uppercase before comparison. This way, case differences will not affect the comparison results.

### Corrected Function:
Here is the corrected version of the `table_exists` function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
```

By converting both the `table` name and the `stdout` to lowercase before comparison, the function will now handle case differences and pass the failing tests.

This fix addresses GitHub issue #896 as well, making the `table_exists` function case insensitive.

Now, the corrected function should pass all the failing test cases with the expected input/output values mentioned earlier.