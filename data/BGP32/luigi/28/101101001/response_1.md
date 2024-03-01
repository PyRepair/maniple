### Bug Explanation
The bug in the `table_exists` function arises from the condition `return stdout and table in stdout`. This condition checks if the `table` is contained in the `stdout` string, but it is not handling cases where the table name is in a new line after the `OK` response. This causes the function to incorrectly determine if the table exists or not.

### Bug Fix Strategy
To fix this bug, we need to modify the condition to properly handle cases where the table name follows the `OK` response on a new line. We can split the `stdout` string by new lines and then check if the `table` is in any of those lines.

### Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        stdout_lines = stdout.split('\n')
        return any(table in line for line in stdout_lines)
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

By splitting the `stdout` string by new lines, we can now correctly check if the table name exists in any line of the output, ensuring the function behaves as expected in all scenarios provided by the failing test cases.