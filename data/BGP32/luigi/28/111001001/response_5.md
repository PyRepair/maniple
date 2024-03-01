### Bug Explanation
The bug in the `table_exists` function lies in the conditional check of whether the `table` exists in the `stdout` output. The current implementation checks if the `table` string is directly present in the `stdout`, which can lead to false positives if the `table` name is a substring of another table name in the `stdout`.

For example, in Case 2 where `table` is `'MyTable'` and `stdout` is `'OK\nmytable'`, the function incorrectly returns `True` because the string `'mytable'` contains `'MyTable'`. This is not the desired behavior as the function should only return `True` if the exact table name exists in the output.

### Bug Fix Strategy
To fix this bug, we need to modify the conditional check to ensure that the full table name matches exactly in the `stdout`. One way to achieve this is by splitting the `stdout` into lines and checking each line individually for an exact match with the `table` name.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By splitting `stdout` into lines using `split('\n')`, we ensure that the function only returns `True` when the exact `table` name matches a line in the `stdout`. This corrected version should provide the desired behavior and prevent false positives in the table existence checking.