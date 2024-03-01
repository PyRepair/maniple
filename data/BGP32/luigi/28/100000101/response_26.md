## Bug Explanation
The bug in the provided function lies in the comparison of the table name in the `stdout` variable. When checking if the table exists, the function is not handling the case sensitivity of table names properly. In some cases, the table name may be returned in different cases (uppercase/lowercase) than the one provided, leading to a false negative result.

## Bug Fix Strategy
To fix the bug, we need to make sure that the comparison between the expected table name and the tables listed in the `stdout` variable is case-insensitive. This can be achieved by converting both strings to the same case (either lowercase or uppercase) before comparing them.

## Corrected Function
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.split("\n"))
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        return bool(stdout)
``` 

The corrected function makes the table name comparison case-insensitive by converting both the expected table name and the tables returned in the `stdout` variable to lowercase before comparing them. This ensures that the function correctly identifies whether the table exists or not.