### Problem Analysis
1. The `table_exists` function in the `HiveCommandClient` class checks if a table exists in a specified database with an optional partition.
2. The bug arises from the case sensitivity issue where table names are compared directly against the output from Hive, which is case insensitive.
3. The bug affects the functionality of checking table existence when table names are provided in different cases.
4. To fix the bug, we need to make the comparison case insensitive by converting both the table name and the Hive output to lowercase for a consistent comparison.

### Bug Fix Strategy
1. Modify the `table_exists` function to convert the `table` name to lowercase before comparison.
2. Convert the output `stdout` from Hive to lowercase for comparison with the lowercase `table` name.
3. This approach will ensure a case-insensitive check for table existence.

### Corrected Version of the Function
```python
    def table_exists(self, table, database='default', partition=None):
        if partition is None:
            stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
    
            return stdout and table.lower() in stdout.lower()
        else:
            stdout = run_hive_cmd("""use %s; show partitions %s partition
                                (%s)""" % (database, table, self.partition_spec(partition)))
    
            if stdout:
                return True
            else:
                return False
``` 

By implementing the changes mentioned above, the `table_exists` function will now perform a case-insensitive comparison when checking the existence of tables in the specified database.