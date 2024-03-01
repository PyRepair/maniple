### Bug Explanation
The bug in the `table_exists` function is related to how the function handles the output of the `run_hive_cmd` function. In the current implementation, the function checks for the presence of the table in the output using `table in stdout`, but this can lead to unexpected results when there are additional characters in the output.

For example, in the failing test case for the table "MyTable", the returned value includes additional characters ("OK\nmytable") along with the table name. Since the function only checks for the exact table name matching in the output, it fails to identify the table, leading to the test failure.

### Bug Fix Strategy
To fix the bug, we need to modify the function so that it correctly identifies the presence of the table name in the output, regardless of additional characters. One way to achieve this is by splitting the output into lines and checking each line for the table name.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return any(table == line.strip() for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By using the corrected function above, the function will split the output into lines and check each line for the presence of the table name, ensuring that it can handle cases where additional characters are included in the output. This modification should resolve the issue and make the function more robust.