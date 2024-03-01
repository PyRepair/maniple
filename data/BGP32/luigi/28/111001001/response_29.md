### Bug Explanation
The bug in the `table_exists` function arises from the condition used to check if a table exists in the Hive database. When checking for the table's existence without a specified partition, the function looks for the exact table name in the output from the Hive command. However, the bug occurs due to case sensitivity in table names; the function does not account for case sensitivity, leading to incorrect results when comparing table names.

### Bug Fix Strategy
To fix the bug, we need to make the comparison case-insensitive when checking if the table exists in the Hive database. We can achieve this by converting both the table name from the Hive output and the provided table name to lowercase before comparison.

### Corrected Version
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

In the corrected version, both the provided table name and the table names from the Hive command output are converted to lowercase before comparison, ensuring a case-insensitive check.