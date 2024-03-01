### Bug Analysis
The buggy function `table_exists` has an issue with the condition checking the presence of a table in the database. The problem arises when checking the output of the `run_hive_cmd` function. The bug is caused by improperly parsing the stdout data from the Hive command result.

### Bug Fix Strategy
To fix the bug, we need to properly parse the stdout data returned from the `run_hive_cmd` function to check for the existence of the table. We need to modify the condition that checks if the table exists based on the parsed stdout data.

### Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
        return stdout and table.lower() in stdout.lower()  # Fix to ignore case differences
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                         (%s)""" % (database, table, self.partition_spec(partition)))
    
        return bool(stdout)  # Fix to return the boolean value directly
``` 

### Updated function explanation:
1. Modified the condition in the if block to check for the table name in a case-insensitive manner.
2. Removed the unnecessary condition in the else block and directly returned the boolean value based on the stdout value.