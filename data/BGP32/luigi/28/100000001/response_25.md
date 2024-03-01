## Analysis:
1. The `table_exists` function checks if a table exists in the specified Hive database.
2. There are two branches in the function: one for when `partition` is None, and another for when `partition` is specified.
3. The function uses a `run_hive_cmd` function to interact with Hive.
4. The bug could be related to the way the command is run or how the output is checked for table existence.

## Bug Explanation:
When `partition` is specified, the string formatting in the `run_hive_cmd` call looks suspicious. The placeholders `%s` might cause incorrect command formation, potentially leading to errors in checking table existence.

## Bug Fix Strategy:
To fix the bug, we should ensure that the command string in `run_hive_cmd` is formatted correctly by properly placing placeholders and formatting the strings for database, table, and partition within the command string.

## Corrected Version:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2});".format(database, table, self.partition_spec(partition)))

        return stdout is not None
``` 

In the corrected version, I have fixed the string formatting in the `run_hive_cmd` call when partition is specified. The placeholders are now properly used and formatted to create the correct command for checking table existence. The function will now return `True` if the table exists and `False` if it does not.