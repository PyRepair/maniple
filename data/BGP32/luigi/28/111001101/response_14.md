## Bug Explanation
The bug in the `table_exists` function stems from how the conditionals are set up to check for the existence of a table in a Hive database. When a partition is provided, the function incorrectly uses triple quotes for the Hive command string, leading to issues with formatting and lack of proper table existence checking under such conditions.

## Bug Fix Strategy
To fix the bug, we need to ensure that the Hive command string is correctly constructed for both cases when a partition is provided and when it's not. It's essential to maintain proper formatting and logic to accurately determine the table's existence in the Hive database.

## The corrected version of the buggy function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}"'.format(database, table))
    
        return stdout and table in stdout
    else:
        stdout = run_hive_cmd("use {0}; show partitions {1} partition ({2})".format(database, table, self.partition_spec(partition)))
    
        if stdout:
            return True
        else:
            return False
``` 

By correcting the quotes and the formatting of the Hive command strings, the function should now be able to accurately determine the existence of a table in the Hive database with or without a partition.