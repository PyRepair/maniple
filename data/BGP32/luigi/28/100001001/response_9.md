### Bug Explanation
The bug in the current function arises from how the function checks for the existence of a table in a database. The function uses the output of a command (`stdout`) to determine if the table exists. However, the implementation is incorrect in the way it checks the `stdout` variable for the presence of the table name.

In the first case, when the table name is `mytable`, the function will check if `'mytable'` is in `'OK'`, which will always return False, causing the function to incorrectly determine that the table does not exist, even though it does.

In the second case, when the table name is `MyTable`, the function will incorrectly find the lowercase version of the table name in the output `'OK\nmytable'`, causing it to return True even though the table name doesn't match exactly.

### Fix Strategy
To fix this bug, we need to modify the way the function checks for the presence of the table name in the `stdout` variable. One way to do this is to split the `stdout` variable by newlines and then check if the table name exactly matches any of the lines.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        table_list = stdout.split('\n')
        return table in table_list
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

In the corrected version, we split the `stdout` variable by newlines into a list of tables and then check if the table exactly matches any of the tables listed. Additionally, we simplify the check for the existence of the table in the partitioned case by directly converting the `stdout` variable to a boolean value.