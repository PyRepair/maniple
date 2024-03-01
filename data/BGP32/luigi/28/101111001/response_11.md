### Bug Explanation:

The bug in the `table_exists` function is due to the way it checks if a table exists in the specified database. The function runs a Hive command to check for the existence of the table by using `show tables` or `show partitions` commands, depending on the presence of a partition. However, the bug lies in how the function interprets the output of the command and determines if the table exists.

The buggy logic checks if the table name is contained in the output of the command. This check is incorrect because it only looks for a substring match, rather than checking the exact table name. This results in false positives where the table name could be a part of another string in the output.

### Bug Fix Strategy:

To fix the bug, we need to modify the logic for checking the existence of the table to ensure that it matches the exact table name. We can achieve this by splitting the output into lines and then comparing each line with the exact table name.

Additionally, for the case where a partition is specified, we need to modify the logic to handle the partition information correctly and ensure that the function returns `True` only if the specified table and partition exist in the database.

### Corrected Version of the Function:

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        if stdout:
            tables = [line.strip() for line in stdout.split('\n')]
            return table in tables
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
    
        if stdout:
            partitions = [line.strip() for line in stdout.split('\n')]
            partition_info = '{}={}'.format(*partition.items()[0])
            return partition_info in partitions
        else:
            return False
```

By splitting the output into lines and comparing each line against the exact table name, we ensure that the function accurately determines the existence of the table. The same approach is taken for checking the existence of partitions when specified.