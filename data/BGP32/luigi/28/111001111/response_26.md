### Identified Bug:
The bug in the `table_exists` function is that it does a case-sensitive check when verifying if a table exists in Hive. This leads to failures when comparing tables with different letter cases.

### Cause of the Bug:
The bug occurs because the function checks for an exact match between the table name provided and the results returned from Hive, without considering the case sensitivity of the comparison.

### Proposed Fix:
To fix the bug and make the `table_exists` function case insensitive, we need to convert both the table name and the results from Hive to lowercase before performing the comparison.

### Corrected Function:
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

### Explanation:
The corrected version of the function converts both the table name and the retrieved results to lowercase before performing the comparison, making the check case insensitive. This change addresses the issue described in the GitHub report and ensures that table existence is verified accurately, regardless of the letter case used for the table names.