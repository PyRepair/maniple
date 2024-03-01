### Bug Explanation
The bug in the `table_exists` function arises from the way it checks for the existence of a table in Hive. In the cases provided:
- In Case 1, when the table name is 'mytable' and the stdout value returned by `run_hive_cmd` is 'OK', the function incorrectly returns `False`.
- In Case 2, when the table name is 'MyTable' and the stdout value returned by `run_hive_cmd` is 'OK\nmytable', the function incorrectly returns `False`.
- In Case 3, when the table name is 'mytable' and the stdout value returned by `run_hive_cmd` is 'OK', the function incorrectly returns `False`.
- In Case 4, when the table name is 'MyTable' and the stdout value returned by `run_hive_cmd` is 'OK\nmytable', the function incorrectly returns `False`.

The bug stems from how the function checks if the table exists in the stdout returned by the `run_hive_cmd` function. The function expects the table name to be an exact match in the stdout, which leads to incorrect results.

### Fix Strategy
To fix this bug, we need to modify the comparison of the table name in the stdout. Instead of a direct comparison, we should split the stdout by newline characters and then check if the table name exists in any of the lines.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        return stdout and table in stdout.split("\n")
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By splitting the stdout by newline characters and checking if the table name exists in any of the lines, the corrected function will now correctly determine whether the table exists.