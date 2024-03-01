### Bug Explanation

The bug in the `table_exists` function is that it directly checks if the `table` name exists in the `stdout` output from the `run_hive_cmd` function without considering the case sensitivity of the table name. The issue arises when the table names have different case variants than what is provided in the function call.

### Bug Fix Strategy

To fix the bug and make the `table_exists` function case insensitive, we need to modify the comparison logic. We should convert both the `table` name and the `stdout` content to lowercase before checking for existence.

### Corrected Version of the Function

Here is the corrected version of the `table_exists` function that addresses the case sensitivity issue:

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

By converting both the `table` name and the `stdout` content to lowercase before comparison, the function will now correctly identify the existence of the table irrespective of the case used in the function call.

This corrected version aligns with the suggestion made in the GitHub issue to make the `table_exists` function case insensitive to prevent case-related failures.