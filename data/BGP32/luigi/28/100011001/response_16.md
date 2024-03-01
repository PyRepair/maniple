### Bug Analysis:
The bug in the `table_exists` function lies in the conditional check that determines whether a table exists in the database. In the `if` block where no partition is specified, the function checks if the table name exists in the output of the `show tables` command. However, in the `else` block where a partition is specified, the function checks if the output of the `show partitions` command is not empty.

The bug seems to be related to the comparison of the output against the table name in the `if` block. The function should check if the table name is present in the output by splitting the lines in the output and then checking.

### Bug Fix Strategy:
To fix the bug, we need to modify the comparison of the output against the table name in the `if` block. We should split the lines in the output and then check if the table name is present in one of the lines.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        return any(line.strip() == table for line in stdout.split('\n'))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        return bool(stdout)
``` 

In the corrected version, the `table_exists` function now correctly splits the output and checks if the table name exists in the list of lines when there is no partition specified. For the case where a partition is specified, the function directly checks if the output is not empty, as that condition is sufficient to determine table existence.