### Bug Explanation
The bug in the provided function `table_exists` lies in the condition checking for the existence of a table. In the code, whether a table exists in the database is determined by whether the table name is present in the output received from the `run_hive_cmd` function. However, the current implementation fails to account for case-sensitive table names. This discrepancy leads to incorrect evaluations of table existence in some scenarios (i.e., when table names have different cases).

### Fix Strategy
To fix this bug, we need to modify the comparison operation between the table name and the output received from `run_hive_cmd` to be case-insensitive. By converting both strings to lowercase before comparison, we can ensure that the function correctly identifies the existence of a table regardless of the case.

### Corrected Version
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in stdout.lower()
    else:
        stdout = run_hive_cmd("""use {0}; show partitions {1} partition
                            ({2})""".format(database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
``` 

In the corrected version, both the `table` and the `stdout` strings are converted to lowercase using the `lower()` function to ensure a case-insensitive comparison, thus addressing the bug mentioned.