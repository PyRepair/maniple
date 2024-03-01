### Bug Analysis
The buggy function `table_exists` is intended to check if a table exists in a given database. The bug seems to be related to how the function handles the `stdout` variable and checks for the existence of the table.

1. In the first branch of the `if` statement, the function checks if the table name exists in the `stdout` variable, but it should be checking if the table name is found in each line of the `stdout`, as `run_hive_cmd` might return multiple lines.
   
2. In the second branch of the `if` statement, the function should return `True` if there's any output in `stdout`, rather than just checking if `stdout` exists.

### Bug Fix Strategy
To fix the bug in the `table_exists` function:
1. Split the `stdout` by newline characters to handle multiple lines of output.
2. Check each line of the split `stdout` for the existence of the table name.
3. Simplify the `if` conditions in both branches to correctly determine the existence of the table based on the `stdout` content.

### Corrected Version of the Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return any(table in line for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

This corrected version properly splits the `stdout` by newline characters to handle multiple lines of output and checks each line for the existence of the table name. It also simplifies the `if` conditions in both branches to correctly determine the existence of the table based on the `stdout` content.