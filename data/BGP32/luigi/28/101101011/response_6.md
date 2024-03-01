## Corrected version of the buggy function

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

## Changes Made:
- Modified the return statement in the if block to check `table.lower() in stdout.lower()`.
- Updated the check to be case insensitive, as suggested in the GitHub issue.
- By making both the table name and the output from Hive lower case, we ensure a case-insensitive comparison for table existence.