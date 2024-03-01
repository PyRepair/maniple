### Bug Explanation
The bug in the `table_exists` function lies in the condition where the function checks if the `stdout` contains the `table` or not. In the buggy implementation, the condition `return stdout and table in stdout` is incorrect as it doesn't check for the exact match of the table. Instead, it checks if the table exists in any output, leading to incorrect results.

### Bug Fix Strategy
To fix the bug, we need to modify the condition to validate that the exact table exists in the output. This can be achieved by splitting the `stdout` based on newlines and then checking if the `table` exists in the split lines. If the table exists as a separate entity in the `stdout`, we return `True`, otherwise `False`.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

By splitting the `stdout` based on newlines and then checking if the `table` exists in those lines, we ensure that the table is an exact match, fixing the bug and aligning the function with the expected behavior.