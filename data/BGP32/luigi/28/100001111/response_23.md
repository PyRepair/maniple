## Bug Fix:

### Bug Explanation:
The bug in the `table_exists` function arises from case sensitivity when comparing the table names retrieved from Hive. The function compares the table name directly with the tables listed in the stdout, which can lead to failures due to case mismatches. The issue described on GitHub highlights the need for case-insensitive comparison to handle tables' names correctly.

### Bug Fix Strategy:
To fix this bug, we need to convert both the table name and the stdout output to lowercase before comparison. This will ensure a case-insensitive match and address the problem described in the GitHub issue.

### Updated `table_exists` Function:
```python
def table_exists(self, table, database='default', partition=None):
    if partition is None:
        stdout = run_hive_cmd('use {0}; show tables like "{1}";'.format(database, table))

        return stdout and table.lower() in map(str.lower, stdout.splitlines())
    else:
        stdout = run_hive_cmd("""use %s; show partitions %s partition
                            (%s)""" % (database, table, self.partition_spec(partition)))

        if stdout:
            return True
        else:
            return False
```

### Changes Made:
1. Converted `table` to lowercase before comparison: `table.lower()`.
2. Converted `stdout` to lowercase before comparison: `map(str.lower, stdout.splitlines())`.

By making these changes, the function now performs case-insensitive comparisons, addressing the bug and aligning with the solution proposed in the GitHub issue.