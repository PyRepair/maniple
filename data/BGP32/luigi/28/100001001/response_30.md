### Analysis:
The buggy function `table_exists` checks if a table exists in the specified database using Hive commands. The bug seems to be related to the comparison of the table name with the output from the Hive command.

### Issue:
The bug arises from the comparison method used for checking the existence of the table. It currently checks if the table name is contained in the output string from the `run_hive_cmd` function, which is not a reliable method. Case 2 demonstrates this issue where the table name 'MyTable' is mistakenly identified as existing in the output 'OK\nmytable'.

### Fix:
To fix this bug, a more accurate approach would be to split the output by newline characters and then check if the exact table name exists in the list of table names. This way, we can ensure a precise match.

### Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')

        return table in tables

    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

By splitting the output and checking if the table name exactly matches one of the tables returned by the Hive command, we ensure a more accurate determination of table existence.