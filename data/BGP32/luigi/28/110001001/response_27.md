### Analysis
The `table_exists` function in the `HiveCommandClient` class is intended to check if a given table exists in a specific database. The function uses `run_hive_cmd` to execute Hive commands and check for the existence of the table. The bug seems to be related to how the function checks the output of the Hive commands.

### Bug Explanation
The bug lies in how the function checks the presence of the table in the output of the Hive command. The current implementation checks if the table name is directly in the `stdout` string, which can lead to false positives or negatives depending on the actual output of the Hive command. For example, in Case 2, the table name 'MyTable' is part of the output 'OK\nmytable', causing a false positive result.

### Fix Strategy
To fix the bug, we need to improve how the function checks for the existence of the table in the `stdout` of the Hive command output. One way to do this is by splitting the `stdout` into lines and checking each line for an exact match with the table name. This approach will ensure that we are correctly determining the presence of the table in the output.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        
        if stdout:
            tables = stdout.split('\n')  # Split the stdout into lines
            return any(t == table for t in tables)  # Check if the table exists in the list of tables
        else:
            return False
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        if stdout:
            return True
        else:
            return False
``` 

In the corrected version, we split the `stdout` string into lines and then check if the table name exactly matches any of the extracted table names. This approach ensures a more accurate check for the existence of the table in the Hive command output.
