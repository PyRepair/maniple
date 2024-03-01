### Bug Analysis
The bug occurs due to how the function `table_exists` handles the output `stdout` from the `run_hive_cmd` function. The current implementation checks if `table` is in `stdout` to determine if the table exists. However, the implementation does not handle cases where the table name might be part of another word in the output, like in the test with table name 'MyTable' where 'mytable' was present in the output.

### Bug Explanation
In Case 2, the `stdout` has the value `'OK\nmytable'`, which causes the function to incorrectly return False because it does a simple substring check. The condition `table in stdout` would return True here since 'mytable' is present in the output, but this is not desired behavior.

### Bug Fix Strategy
To fix the bug, we need to improve the way the function checks if the table exists. Instead of a simple substring check, we should ensure that the extracted table name from the output is an exact match to the provided table name.

### Corrected Function

```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table)).strip()
        
        tables = stdout.split('\n')
        return table in tables
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition (%s)""" % (database, table, self.partition_spec(partition))).strip()
        
        return bool(stdout)
``` 

The corrected function splits the output by newline character and then checks if the exact table name is present in the list of tables. The `.strip()` method is also used to clean up any leading or trailing whitespaces in the output. In the else case, it simply checks if `stdout` has any content which would imply that the table exists. This ensures a more robust check for table existence.