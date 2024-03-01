### Bug Explanation
The bug arises from the function `table_exists()` not accounting for case sensitivity when comparing the table name in Hive to the provided table name. The function directly checks for the exact match of the table name in the output from Hive, leading to failures in cases where there is a case mismatch between the provided table name and the actual table name in Hive.

### Bug Fix Strategy
To fix the bug and make the `table_exists()` function case insensitive, we need to modify the comparison of the table name from Hive with the provided table name. By converting both the table name from Hive and the provided table name to lowercase (or uppercase), we can ensure a case-insensitive comparison.

### Corrected Function
Here is the corrected version of the `table_exists()` function with the necessary modifications to make it case insensitive:

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

In the corrected version:
1. Both the `table` and the table names in the `stdout` are converted to lowercase before comparison using `lower()` to make the check case insensitive.
2. This modification ensures that the provided table names are compared irrespective of their cases, addressing the issue reported on GitHub about case sensitivity.