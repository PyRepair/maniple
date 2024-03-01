## Bug Explanation
The bug in the provided function lies in the comparison condition for checking if the table exists. In the first case, the function checks if the table name is in the output of the 'show tables' command in Hive. However, the comparison is case-sensitive, which leads to failures in cases where the table names have different case variations.

In the second case, the function incorrectly compares the table name without accounting for case sensitivity, leading to incorrect results when the table names don't match exactly.

## Bug Fix Strategy
To fix the bug, we need to ensure that the comparison of table names is case-insensitive to handle variations in case correctly. We can achieve this by converting both the table names to lowercase before comparing them.

## Corrected Version of the Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

This corrected version of the function converts both the table name and the names retrieved from Hive to lowercase before comparing them, ensuring a case-insensitive check for table existence.