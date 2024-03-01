### Bug Explanation
The bug in the `table_exists` function lies in the logic where the function checks if the table exists in the database. In the case of table names containing uppercase letters (like 'MyTable'), the comparison between table names fails due to case sensitivity.

### Bug Fix Strategy
To fix the bug, we need to make the comparison between table names case-insensitive. One approach is to convert both table names to lowercase or uppercase before comparing them.

### Corrected Function
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

This corrected function converts both the input table name and the names retrieved from `stdout` to lowercase before comparison, ensuring a case-insensitive comparison. This fix should make the function behave correctly and pass the failing tests.