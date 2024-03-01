The bug in the `table_exists` function arises from the comparison logic used to check if a table exists in the given database. The function relies on the output of the `run_hive_cmd` function to determine the existence of the table, but the comparison logic is flawed.

### Bug Explanation
- In the first condition where `partition` is `None`, the function attempts to check if the `table` string is in the `stdout` string obtained from running the Hive command. This comparison would fail if the `table` name is a substring of another table name in the output.
- In the second condition where `partition` is not `None`, the function constructs a Hive command using `%s` formatting where the `table` name and the output of `self.partition_spec(partition)` are inserted, but the logic to validate the existence of the table is not based on the command output.

### Bug Fix Strategy
1. For the first condition, we need to split the lines in `stdout` to ensure an exact match with the table name.
2. For the second condition, we need to check for the table's existence based on the output of the Hive command returned by `run_hive_cmd`.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))
        tables = stdout.split('\n')
        
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))
        
        return stdout is not None  # Check if the command output is not empty to confirm table existence
``` 

This corrected version resolves the comparison issues and ensures an accurate check for table existence in the specified database.