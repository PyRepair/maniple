### Bug Explanation
The bug in the `table_exists` function is caused by the logic that checks for the presence of the table in the stdout. In the first case, when `stdout` is equal to `'OK'`, the function incorrectly evaluates `'OK' and table in stdout`, which results in the function returning `False` instead of `True`. 

In the second case, when `stdout` is equal to `'OK\nmytable'`, the function incorrectly evaluates `table in stdout`, which results in the function returning `False` instead of `True`.

The issue stems from the incorrect evaluation of the presence of the table in the `stdout`.

### Bug Fix Strategy
To fix the bug, we need to ensure that the function correctly processes the `stdout` to determine if the table exists. We can split the `stdout` into lines and then check if the table exists in any of the lines. This adjustment will prevent the function from returning `False` even when the table is present in the `stdout`.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table)).strip()

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition))).strip()

        return any([table in line for line in stdout.split('\n')])
``` 

By splitting `stdout` into lines and checking for the existence of the table in each line, the corrected function should now correctly determine if the table exists in the database.