### Analysis:
- The `table_exists` function checks for the existence of a table in a Hive database. 
- The bug occurs because the function performs a case-sensitive check between the provided table name and the output received from the Hive command, leading to test failures when the case of the table names does not match.
- The output from the `run_hive_cmd` function is compared directly with the table name without any case normalization, causing the bug.
- The GitHub issue #896 and its description clearly highlight the need to make the `table_exists` function case insensitive.

### Bug Cause:
- The bug is caused by the case-sensitive comparison between the provided table name and the output of the Hive command in the `table_exists` function.

### Fix Strategy:
- To fix the bug, we should make the comparison case insensitive by converting both the table name and the output to lowercase before comparing them.

### Corrected Version of the `table_exists` Function:
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
The corrected version of the `table_exists` function fixes the bug by converting both the provided table name and the output to lowercase before performing the comparison. This change makes the function case-insensitive, addressing the test failures and aligning with the suggested fix in the GitHub issue #896.