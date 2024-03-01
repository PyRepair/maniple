### Bug Explanation
The bug in the `table_exists` function lies in the condition to check if the table exists. In the first case, the function checks if the table is in the output stdout directly, which is the expected behavior. However, in the second case where the table name is 'MyTable', the function fails to handle case-insensitive table name comparisons correctly. The condition `table in stdout` is case-sensitive, causing the test to fail.

### Bug Fix Strategy
To fix the bug, we need to make the comparison case-insensitive. One way to achieve this is by converting both the table name and the stdout to lowercase before comparing them.

### Corrected Version
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

By converting both the `table` and `stdout` to lowercase before comparing, we ensure that the comparison in `table in stdout` is now case-insensitive, allowing the function to correctly determine if the table exists in the database.