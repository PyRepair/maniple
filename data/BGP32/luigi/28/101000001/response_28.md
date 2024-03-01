## Analysis:
1. The `table_exists` function checks whether a table exists in a Hive database.
2. It calls the `run_hive_cmd` function to execute Hive commands.
3. When `partition` is not None, the `table_exists` function tries to show partitions for a specific table and partition.

## Bug Location:
The bug is located in the conditional statement checking the existence of partitions. The string formatting and concatenation may not be correctly forming the command.

## Bug Cause:
The bug occurs due to incorrect string formatting when constructing the Hive command in the `table_exists` function for the case when `partition` is not None. The use of `%s` placeholders does not properly format the command.

## Bug Fix:
To fix the bug, update the string formatting in the else block to use the `.format` method for proper formatting.

## Corrected Version:
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