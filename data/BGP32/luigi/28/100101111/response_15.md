### Bug Explanation:
The bug in the `table_exists` function arises from the fact that the comparison between the table name and the tables listed in the Hive response is case-sensitive. This causes the function to incorrectly determine if a table exists or not based on the case of the table name provided.

When comparing the provided table name with the tables in the response from Hive, the function does not take into account the case sensitivity of the table names. This leads to inconsistencies when checking for table existence.

### Solution Strategy:
To fix the bug and make the `table_exists` function case-insensitive, we need to ensure that the comparison between the table names is done in a case-insensitive manner. By converting both the provided table name and the table names in the Hive response to lowercase before comparison, we can address the case sensitivity issue.

### Corrected Function:
Here is the corrected version of the `table_exists` function:

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

### Justification:
In the corrected function, both the provided `table` name and the table names in the `stdout` response are converted to lowercase using `lower()` before comparison. This ensures that the comparison is done in a case-insensitive manner, resolving the bug reported in the failing test cases and GitHub issue. The function now correctly determines whether a table exists in Hive regardless of the case of the table name provided.