### Bug Explanation
The bug in the `table_exists` function lies in the comparison of the table name in the `stdout` variable. The function checks if the table is in `stdout` by simply using `table in stdout`. This check is problematic because it can lead to false positives or negatives due to the presence of other characters beside the table name in `stdout`. For example, in Case 2, where `table` is 'MyTable' and `stdout` is 'OK\nmytable', the comparison would fail even though 'mytable' is present in the `stdout`.

### Bug Fix Strategy
To fix this bug, we need to parse the `stdout` properly to extract only the table names for comparison. We should split the `stdout` by newline characters and then check if the table name is in the resulting list.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By modifying the logic as described above in the corrected function, the bug should be fixed and all the failing test cases should pass successfully.