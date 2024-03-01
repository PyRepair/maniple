### Explanation:
The bug in the `table_exists` function lies in the comparison between the table name and the output from the Hive command. Hive returns table names in lowercase, causing the comparison to fail if the input table name is in a different case.

The failing tests are designed to cover scenarios where the table name is provided in different cases than what Hive returns. The function compares the input table name directly with the output from Hive without considering case sensitivity, leading to the test failures.

### Bug Fix Strategy:
To fix the bug, we need to ensure that the comparison between the table name and the Hive output is case-insensitive. By converting both strings to lowercase before comparison, we can achieve consistent behavior regardless of the case of the input.

### Code Fix:
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

By converting `table` and `stdout` to lowercase before comparison (`table.lower()` and `stdout.lower()`), we ensure a case-insensitive check for table existence in the Hive output.

After applying this fix, the function should pass the failing tests and meet the expected input/output values, resolving the issue indicated on GitHub.