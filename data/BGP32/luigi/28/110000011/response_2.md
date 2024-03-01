Potential error locations within the buggy function:
1. The comparison of the table name 'table' with the names in the 'stdout' variable might lead to case sensitivity issues.
2. The 'stdout' variable might not be properly formatted to handle case insensitive comparisons.

Cause of the bug:
1. The bug is caused by the case sensitivity of the comparison between the table name and the names in the 'stdout' variable. Since Hive is case insensitive, the table names might differ in case and cause the function to return incorrect results.

Strategy for fixing the bug:
1. To fix the bug, it is suggested to convert both the table name and the 'stdout' variable to lowercase before comparison. This way, case sensitivity issues can be resolved.

Corrected version of the function:
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

By converting both the table name and the 'stdout' variable to lowercase before comparison, the function will now be case insensitive and provide the correct results for table existence check.