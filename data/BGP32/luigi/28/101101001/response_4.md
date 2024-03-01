### Identified Bug
The bug in the `table_exists` function is that it only checks if the table name is present in the output from the `run_hive_cmd` function, without considering the case sensitivity of the table name. This results in failing tests when the table name cases are different.

### Bug Explanation
- In Case 1 and Case 3, the input table name is 'mytable', and the returned `stdout` is 'OK'. The function incorrectly returns `False` since it only checks for an exact match of the table name in `stdout`.
- In Case 2 and Case 4, the input table name is 'MyTable', and the returned `stdout` is 'OK\nmytable'. The function incorrectly returns `False` in Case 2 since it checks for an exact match, even though the table name is present with different cases in the `stdout`.

### Fix Strategy
To fix the bug, we need to modify the `table_exists` function to check for the table name case-insensitively in the `stdout`.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return stdout and any(t.lower() == table.lower() for t in stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

By using `t.lower() == table.lower()` we compare the table names case-insensitively, ensuring that the function correctly identifies the presence of the table in the `stdout`.