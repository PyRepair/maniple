### Identified Bug:
The bug in the `table_exists` function is that it is not case insensitive when comparing the table name from the output of the `run_hive_cmd` function. This leads to failures when the table names have different case variations.

### Cause of the Bug:
1. The function `table_exists` retrieves the table names from the Hive command output using `run_hive_cmd`.
2. The check to verify if the table exists is performed by directly comparing the returned table name from Hive with the input table name in a case-sensitive manner.
3. If the case of the input table name and the table name in Hive output do not match, the comparison fails, resulting in false negatives.

### Fix Strategy:
To fix the bug, the comparison between the input table name and the table name from the Hive output should be made case insensitive. This ensures that the function works correctly regardless of the case of the table names.

### Corrected Version:
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

In the corrected version, both the input table name and the table name retrieved from Hive are converted to lowercase for comparison, making the `table_exists` function case insensitive. This fix addresses the issue reported on GitHub and ensures that the function works correctly in all scenarios.