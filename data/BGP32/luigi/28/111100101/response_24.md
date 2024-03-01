### Analysis
The buggy function `table_exists` is not handling the output of the `run_hive_cmd` function correctly. In the first case, it expects a simple string output, while in the second case, it expects a string with table names separated by newline characters. The function also fails to check for the presence of the table name in the output correctly.

### Bug Cause
The bug occurs because the function does not correctly parse the output of the `run_hive_cmd` function to check for the existence of the table in the database. In the first case, the function simply checks if the table name is equal to a single line of output. In the second case, the function incorrectly assumes that the table name will be in a separate line in the output.

### Bug Fix
To fix this bug, we need to modify the `table_exists` function to correctly parse the output of the `run_hive_cmd` function. We need to split the output by newline characters and then check if the table name exists in any of the lines.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout.split('\n')
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return True if stdout else False
``` 

By splitting the `stdout` by newline characters and checking if the `table` exists in any of the lines, we ensure that the function correctly identifies the presence of the table in the database.