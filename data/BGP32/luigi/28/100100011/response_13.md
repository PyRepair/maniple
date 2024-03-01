### Analysis:
1. The `table_exists` method is supposed to check for the existence of a table in a Hive database, but it currently has a bug related to case sensitivity.
2. The bug stems from the comparison between the table name and the output from the Hive command, potentially causing test failures due to case differences.
3. The issue reported on GitHub highlights this problem where tables with different case formatting may not be correctly identified.
4. To fix the bug, the comparison should be made case-insensitive to ensure that the method works correctly in all scenarios.

### Bug Fix:
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
- The correction involves converting both the table name and the Hive command output to lowercase before comparison.
- This change ensures that the comparison is case-insensitive, as suggested in the GitHub issue.
- By making this adjustment, the `table_exists` method will correctly identify tables regardless of their case formatting, resolving the reported bug.