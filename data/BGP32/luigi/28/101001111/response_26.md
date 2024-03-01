### Identified Bug:
The bug in the `table_exists` function is that it doesn't handle case insensitivity when comparing the table name with the output from the Hive command. This results in failing tests when the table names have different cases.

### Cause of the Bug:
The bug arises because the function compares the exact table name with the output from Hive, which might be in a different case. If the case of both strings doesn't match, the comparison fails, leading to incorrect results.

### Fix Strategy:
To fix the bug, we need to make the comparison case insensitive by converting both the table name and the output from Hive to lower case before checking for existence.

### Corrected Code:
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

### Summary:
The corrected function now converts both the table name and the Hive output to lower case before comparing for existence, making the comparison case insensitive. This fixes the bug and aligns with the expected behavior based on the failing tests and the GitHub issue.