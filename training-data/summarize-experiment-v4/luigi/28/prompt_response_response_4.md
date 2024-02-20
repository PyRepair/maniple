### Bug Location
The bug is likely caused by the comparison between the table name and the stdout not being case insensitive, leading to a mismatch in comparison when the table name contains uppercase letters.

### Bug Cause
The bug is caused by the comparison between the table name and the stdout not being case insensitive. The issue was raised in GitHub, indicating that table names are sometimes defined in capitalized form, but Hive returns them in lower case, causing the table_exists function to fail.

### Approach for Fixing the Bug
To fix the bug, we need to make the comparison between the table name and the stdout case insensitive.

### Corrected Code
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