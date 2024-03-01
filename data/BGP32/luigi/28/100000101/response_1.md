## Analysis
The buggy function `table_exists` has two branches, one for when `partition` is None and one for when it is not None. 

In the case where `partition` is None, the function runs a Hive command to show tables in the specified database and checks if the given `table` exists in the output. 

In the case where `partition` is not None, the function runs a Hive command to show partitions for the specified table and partition key. 

The bug seems to be in the logic when `partition` is not None. The function calls `self.partition_spec(partition)` but the result is used incorrectly in formatting the Hive command string.

## Bug
In the branch where `partition` is not None, the bug is in the line:
```
stdout = run_hive_cmd("""use %s; show partitions %s partition
                        (%s)""" % (database, table, self.partition_spec(partition)))
```
The formatting of the string is incorrect, and it is supposed to be:
```
stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))
```

## Updated Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

With this correction, the function should now correctly check for the existence of the table when `partition` is not None.