### Bug Explanation
The bug in the `table_exists` function lies in how the `stdout` variable is being checked. The issue arises from the check `return stdout and table in stdout`. If the `stdout` contains the table name but also contains other information, the function incorrectly returns `True` because `table in stdout` evaluates to `True` even if the table name is just a part of the output.

### Bug Fix
To fix the bug, we need to ensure that the table name in `stdout` is an exact match, not just a substring. One way to do this is by splitting the `stdout` output by lines and checking each line to see if the table name appears separately.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        if stdout:
            return table in stdout.split('\n')
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                              (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By splitting the `stdout` and checking each line for an exact match of the table name, we ensure that the function correctly determines whether the table exists.