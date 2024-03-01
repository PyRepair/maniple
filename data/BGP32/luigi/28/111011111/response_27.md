The bug in the `table_exists` function stems from a case sensitivity issue when comparing the table name extracted from the Hive command output with the provided table name. Hive is case insensitive, so the comparison should also be case insensitive.

### Bug Explanation:
The buggy function `table_exists` compares the table name extracted from the Hive command output with the provided table name. However, the comparison is case-sensitive, leading to test failures when the cases do not match. This issue was highlighted in GitHub issue #896, suggesting that the comparison should be made case insensitive.

### Bug Fix Strategy:
To fix this bug, we need to modify the comparison in the `table_exists` function to be case insensitive. By converting both the table name from the output and the provided table name to lowercase before comparing them, we can ensure that the comparison is not affected by case differences.

### Corrected Version of the Function:
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

By making the comparison case insensitive in the corrected version, the function should now pass the failing tests and address the issue reported on GitHub.